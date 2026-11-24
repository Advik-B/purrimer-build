// Usage: dotnet run -- manifest.json   (written by scripts/showcase.py)
// Fails if an example does not parse, Avalonia logs a warning or error (bindings, properties, layout),
// or the frame cannot be captured.
using System.Text.Json;
using Avalonia;
using Avalonia.Controls;
using Avalonia.Controls.Primitives;
using Avalonia.VisualTree;
using Avalonia.Headless;
using Avalonia.Layout;
using Avalonia.Logging;
using Avalonia.Markup.Xaml;
using Avalonia.Media;
using Avalonia.Media.Imaging;
using Avalonia.Styling;
using Avalonia.Threading;
using Purrimer.Avalonia;
using Purrimer.Showcase;

var manifest = JsonDocument.Parse(File.ReadAllText(args[0])).RootElement;
var outDir = Path.Combine(manifest.GetProperty("out").GetString()!, "avalonia");
Directory.CreateDirectory(outDir);
var scale = manifest.GetProperty("scale").GetDouble();
var pad = manifest.GetProperty("padding").GetDouble();
var themes = new Dictionary<string, ThemeVariant>
{
    ["blanc"] = PurrimerThemes.Blanc,
    ["noir"] = PurrimerThemes.Noir,
    ["light"] = PurrimerThemes.Latte,
    ["dark"] = PurrimerThemes.Mocha,
};

// Longer than the slowest enter transition (duration-sleepy-long, 900ms) with room for slow CI runners.
const int SettleMs = 1500;
// Spinners and other loops stop on their first frame, so screenshots do not change from run to run.
PurrimerMotion.PauseLoops = true;
var sink = new CollectingSink();
Logger.Sink = sink;
AppBuilder.Configure<App>()
    .UseSkia()
    .UseHeadless(new AvaloniaHeadlessPlatformOptions { UseHeadlessDrawing = false })
    .SetupWithoutStarting();

var failures = new List<string>();
foreach (var theme in manifest.GetProperty("themes").EnumerateArray().Select(t => t.GetString()!))
{
    Application.Current!.RequestedThemeVariant = themes[theme];
    foreach (var comp in manifest.GetProperty("components").EnumerateArray())
    {
        var name = comp.GetProperty("name").GetString()!;
        var width = comp.GetProperty("width").GetDouble();
        var height = comp.GetProperty("height").GetDouble();
        var file = comp.GetProperty("files").GetProperty("avalonia").GetString()!;
        var bleed = comp.GetProperty("bleed").GetBoolean();
        var label = $"avalonia/{name}/{theme}";
        sink.Messages.Clear();
        try
        {
            var example = (Control)AvaloniaRuntimeXamlLoader.Load(File.ReadAllText(file), typeof(Card).Assembly);
            if (!bleed) example.VerticalAlignment = VerticalAlignment.Top;
            // Shadows spill past the component, as on the web, so the example root must not clip them.
            example.ClipToBounds = false;
            var frame = new Border
            {
                Width = width,
                Height = height,
                Padding = new Thickness(bleed ? 0 : pad),
                Child = example,
                HorizontalAlignment = HorizontalAlignment.Left,
                VerticalAlignment = VerticalAlignment.Top,
            };
            frame.Bind(Border.BackgroundProperty, frame.GetResourceObservable("PmBgColorDefault"));
            // The headless platform renders at scale 1; a layout transform gives the same pixels as a 2x screen.
            var window = new Window
            {
                Width = width * scale,
                Height = height * scale,
                SizeToContent = SizeToContent.Manual,
                Content = new LayoutTransformControl { LayoutTransform = new ScaleTransform(scale, scale), Child = frame },
            };
            window.Show();
            // Let transitions settle. The animation clock follows real time, so tick for a little longer than the
            // slowest transition.
            var settle = System.Diagnostics.Stopwatch.StartNew();
            while (settle.ElapsedMilliseconds < SettleMs)
            {
                Dispatcher.UIThread.RunJobs();
                AvaloniaHeadlessPlatform.ForceRenderTimerTick();
                Thread.Sleep(16);
            }
            // Popups (ActionMenu, ToolTip) are hosted outside the layout transform above: placed against the scaled
            // target but drawn at scale 1. Scale each one about the point its placement anchors it by.
            foreach (var popup in window.GetVisualDescendants().OfType<Popup>().Where(p => p.IsOpen))
            {
                if (popup.Child?.GetVisualAncestors().OfType<OverlayPopupHost>().FirstOrDefault() is not { } host)
                    continue;
                var origin = popup.Placement switch
                {
                    PlacementMode.Top => new RelativePoint(0.5, 1, RelativeUnit.Relative),
                    PlacementMode.Bottom => new RelativePoint(0.5, 0, RelativeUnit.Relative),
                    PlacementMode.Left => new RelativePoint(1, 0.5, RelativeUnit.Relative),
                    PlacementMode.Right => new RelativePoint(0, 0.5, RelativeUnit.Relative),
                    _ => new RelativePoint(0, 0, RelativeUnit.Relative),
                };
                host.RenderTransformOrigin = origin;
                host.RenderTransform = new ScaleTransform(scale, scale);
            }
            // Controls a component puts straight into the overlay layer (InfoButton's sheet, HoldMenu's layer) fill the unscaled window.
            // Shrink them to the frame's size and scale them back up from the corner.
            if (OverlayLayer.GetOverlayLayer(frame) is { } overlay)
            {
                foreach (var child in overlay.Children.OfType<Control>().Where(c => c is BottomSheet or HoldMenuLayer))
                {
                    child.Width = overlay.Bounds.Width / scale;
                    child.Height = overlay.Bounds.Height / scale;
                    child.RenderTransformOrigin = new RelativePoint(0, 0, RelativeUnit.Relative);
                    child.RenderTransform = new ScaleTransform(scale, scale);
                }
                Dispatcher.UIThread.RunJobs();
            }
            AvaloniaHeadlessPlatform.ForceRenderTimerTick();
            var shot = window.CaptureRenderedFrame();
            if (shot is null) sink.Messages.Add("no frame was rendered");
            else shot.Save(Path.Combine(outDir, $"{name}-{theme}.png"), new PngBitmapEncoderOptions());
            window.Close();
            Dispatcher.UIThread.RunJobs();
        }
        catch (Exception e)
        {
            sink.Messages.Add(e.ToString());
        }
        if (sink.Messages.Count > 0) failures.Add($"{label}\n  " + string.Join("\n  ", sink.Messages));
        else Console.WriteLine($"ok {label}");
    }
}

if (failures.Count > 0)
{
    Console.Error.WriteLine($"\n{failures.Count} Avalonia example(s) failed:\n" + string.Join("\n", failures));
    return 1;
}
return 0;

sealed class CollectingSink : ILogSink
{
    public List<string> Messages { get; } = new();

    public bool IsEnabled(LogEventLevel level, string area) => level >= LogEventLevel.Warning;

    public void Log(LogEventLevel level, string area, object? source, string messageTemplate) =>
        Messages.Add($"{level} [{area}] {source}: {messageTemplate}");

    public void Log(LogEventLevel level, string area, object? source, string messageTemplate, params object?[] propertyValues) =>
        Messages.Add($"{level} [{area}] {source}: {Format(messageTemplate, propertyValues)}");

    static string Format(string template, object?[] values)
    {
        var i = 0;
        return System.Text.RegularExpressions.Regex.Replace(template, @"\{[^}]+\}", m => i < values.Length ? $"{values[i++]}" : m.Value);
    }
}
