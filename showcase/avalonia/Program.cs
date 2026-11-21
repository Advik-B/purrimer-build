// Usage: dotnet run -- manifest.json   (written by scripts/showcase.py)
// Fails if an example does not parse, Avalonia logs a warning or error (bindings, properties, layout),
// or the frame cannot be captured.
using System.Text.Json;
using Avalonia;
using Avalonia.Controls;
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
            while (settle.ElapsedMilliseconds < 700)
            {
                Dispatcher.UIThread.RunJobs();
                AvaloniaHeadlessPlatform.ForceRenderTimerTick();
                Thread.Sleep(16);
            }
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
