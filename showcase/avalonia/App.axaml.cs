using Avalonia;
using Avalonia.Markup.Xaml;

namespace Purrimer.Showcase;

public class App : Application
{
    public override void Initialize() => AvaloniaXamlLoader.Load(this);
}
