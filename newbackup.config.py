# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from libqtile import bar, layout, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

mod = "mod4"
alt = "mod1"
terminal = guess_terminal()

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod, "shift"], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod, "shift"], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod, "shift"], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod, "shift"], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([alt], "Tab", lazy.group.next_window(), desc="Focus next window"),
    Key([alt, "shift"], "Tab", lazy.group.prev_window(), desc="Focus next window"),
    
    Key([mod], "Escape", lazy.window.kill(), desc="Kill focused window"),
    Key([mod], "c", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "shift"], "c", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
]

#groups = [Group(i) for i in [123456789]]

groups = [
    Group("1", spawn = 'code-git'),
    Group("2", spawn = 'google-chrome-stable' ),
    Group("3"),
    # Group("1", matches=Match(wm_class=["code-git-qtile"])),
    Group("4"),
    Group("5"),
    Group("g", label = 'gchat', spawn = 'chromium --app=https://mail.google.com/chat'),
    Group("s", label = 'slack', spawn = 'slack'),
    Group("e", label = 'email', spawn = 'thunderbird')
]

def getIndex(currentGroupName):
    for i in xrange(len(groups)):
        if groups[i].name == currentGroupName:
            return i

def toPrevGroup(qtile):
    currentGroup = qtile.currentGroup.name
    i = getIndex(currentGroup)
    lazy.window.togroup(groups[ (i - 1) % len(groups)].name)

def toNextGroup(qtile):
    currentGroup = qtile.currentGroup.name
    i = getIndex(currentGroup)
    lazy.window.togroup(groups[ (i + 1) % len(groups)].name)

#groups = [
#Group('a', spawn="google-chrome"),
#Group('s', spawn="urxvt"),
#]

# @hook.subscribe.startup_complete
# def complete():
#     groups = []
#     groups.append(Group("1"))
#     groups.append(Group("2"))
#     groups.append(Group("1"))
#     groups.append(Group("4"))
#     #groups.append(Group("4", spawn = "code-git"))
#     #groups.append(Group("5", spawn = "urxvt" ))
#     groups.append(Group("6"))
#     groups.append(Group("7"))


# @hook.subscribe.startup_once
# def startup():
#     for cmd in ['code-git','chromium --class "chromium-qtile"']:
#         subprocess.Popen(cmd)
prevIndex = 0
nextIndex = 2
for i in groups:
    if(nextIndex == len(groups)):
        nextIndex = 0
    
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # go to next group
            Key([mod], "Right", lazy.screen.next_group(),
                desc="Switch to next group"),
            # go to previous group
            Key([mod], "Left", lazy.screen.prev_group(),
                desc="Switch to previous group"),
            # go to next group with tab
            Key([mod], "Tab", lazy.screen.next_group(),
                desc="Switch to next group"),
            # go to previous group with tab
            Key([mod, "shift"], "Tab", lazy.screen.prev_group(),
                desc="Switch to previous group"),
            
            # Key(
            #     [mod, "shift"],
            #     "Right",
            #     lazy.window.togroup(str(nextIndex), switch_group=True),
            #     desc="Switch to & move focused window to next group.",
            # ),

            # mod1 + shift + letter of group = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod1 + shift + letter of group = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )

    prevIndex += 1
    nextIndex += 1

#not working
# keys.append(Key([mod, "shift"], "Left", lazy.function(toPrevGroup)))
# keys.append(Key([mod, "shift"], "Right", lazy.function(toNextGroup)))



layouts = [
    layout.Columns(border_focus_stack=["#d75f5f", "#8f3d3d"], border_width=4),
    layout.Max(),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font="sans",
    fontsize=22,
    padding=1,
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.CurrentLayout(),
                widget.GroupBox(),
                widget.Prompt(),
                widget.WindowName(fontsize=15),
                widget.Chord(
                    chords_colors={
                        "launch": ("#ff0000", "#ffffff"),
                    },     # Key(
            #     [mod, "shift"],
            #     "Right",
            #     lazy.window.togroup(str(nextIndex), switch_group=True),
            #     desc="Switch to & move focused window to next group.",
            # ),
                    name_transform=lambda name: name.upper(),
                ),
                # widget.TextBox("default config", name="default"),
                # widget.TextBox("Press &lt;M-r&gt; to spawn", foreground="#d75f5f"),
                widget.Net(prefix='M', fontsize=18, padding=5, format='{down}↓{up}↑', interface='wlp0s20f3'),
                widget.Systray(),
                # widget.Clock(format="%Y-%m-%d %a %I:%M %p"),
                # %a for day of week
                widget.Volume(fmt='Vol: {}'),
                widget.Memory(measure_mem='G',fontsize=15),
                widget.Clock(format="%m/%d", fontsize=22,padding=10),
                widget.BatteryIcon(format="{percent:2.0%}",padding=5, fontsize=20),
                widget.Clock(format="%I:%M",padding=5, fontsize=22)
                # widget.QuickExit(),
            ],
            25,
            # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"


