from kivy.uix.button import Button
from kivy.uix.spinner import Spinner, SpinnerOption


kv = """
<RoundedButton>:
    markup: True
    background_color: 0,0,0,0
    color: 1,1,1,1
    disabled_color: .8,.8,.8,1
    background_disabled_normal: ''
    height: dp(30)
    size_hint_y: None
    bg_normal: .1,.4,.7,1
    bg_pressed: .2,.5,.8,1
    bg_disabled: .3,.3,.3,1
    bg_normal_2: .3,.6,.9,1
    bg_pressed_2: .4,.7,1,1
    bg_disabled_2: .4,.4,.4,1
    corner_radius: 5
    canvas.before:
        Color:
            rgba: self.bg_disabled if self.disabled else (self.bg_normal if self.state == 'normal' else self.bg_pressed) 
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [self.corner_radius+1,]
        Color:
            rgba: self.bg_disabled_2 if self.disabled else (self.bg_normal_2 if self.state == 'normal' else self.bg_pressed_2)
        RoundedRectangle:
            pos: self.pos[0]+2, self.pos[1]+2
            size: self.size[0]-4, self.size[1]-4
            radius: [self.corner_radius,]


<CloseButton>:
    markup: True
    background_color: 0,0,0,0
    color: 1,1,1,1
    disabled_color: .8,.8,.8,1
    background_disabled_normal: ''
    width: dp(30)
    height: dp(30)
    size_hint_x: None
    size_hint_y: None
    bg_normal: .1,.4,.7,1
    bg_pressed: .2,.5,.8,1
    bg_disabled: .3,.3,.3,1
    bg_normal_2: .3,.6,.9,1
    bg_pressed_2: .4,.7,1,1
    bg_disabled_2: .4,.4,.4,1
    canvas.before:
        Color:
            rgba: self.bg_disabled if self.disabled else (self.bg_normal if self.state == 'normal' else self.bg_pressed) 
        Rectangle:
            pos: self.pos
            size: self.size
        Color:
            rgba: self.bg_disabled_2 if self.disabled else (self.bg_normal_2 if self.state == 'normal' else self.bg_pressed_2)
        Rectangle:
            pos: self.pos[0]+2, self.pos[1]+2
            size: self.size[0]-4, self.size[1]-4


<RoundedSpinnerOption>:
    markup: True
    background_color: 0,0,0,0
    color: 1,1,1,1
    disabled_color: .8,.8,.8,1
    background_disabled_normal: ''
    height: dp(30)
    size_hint_y: None
    bg_normal: .1,.4,.7,1
    bg_pressed: .2,.5,.8,1
    bg_disabled: .3,.3,.3,1
    bg_normal_2: .3,.6,.9,1
    bg_pressed_2: .4,.7,1,1
    bg_disabled_2: .4,.4,.4,1
    corner_radius: 5
    canvas.before:
        Color:
            rgba: self.bg_disabled if self.disabled else (self.bg_normal if self.state == 'normal' else self.bg_pressed) 
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [self.corner_radius+1,]
        Color:
            rgba: self.bg_disabled_2 if self.disabled else (self.bg_normal_2 if self.state == 'normal' else self.bg_pressed_2)
        RoundedRectangle:
            pos: self.pos[0]+2, self.pos[1]+2
            size: self.size[0]-4, self.size[1]-4
            radius: [self.corner_radius,]


<RoundedSpinner>:
    size_hint: (None, None)
    width: dp(64)
    height: dp(30)
    sync_height: True
    background_disabled_normal: ''
    background_color: 0,0,0,0
    color: 1,1,1,1
    disabled_color: .8,.8,.8,1
    corner_radius: 5
    bg_normal: .1,.4,.7,1
    bg_pressed: .2,.5,.8,1
    bg_disabled: .3,.3,.3,1
    bg_normal_2: .3,.6,.9,1
    bg_pressed_2: .4,.7,1,1
    bg_disabled_2: .4,.4,.4,1
    canvas.before:
        Color:
            rgba: self.bg_disabled if self.disabled else (self.bg_normal if self.state == 'normal' else self.bg_pressed) 
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [self.corner_radius+1,]
        Color:
            rgba: self.bg_disabled_2 if self.disabled else (self.bg_normal_2 if self.state == 'normal' else self.bg_pressed_2)
        RoundedRectangle:
            pos: self.pos[0]+2, self.pos[1]+2
            size: self.size[0]-4, self.size[1]-4
            radius: [self.corner_radius,]

"""


class RoundedButton(Button):
    pass


class CloseButton(Button):
    pass


class RoundedSpinnerOption(SpinnerOption):
    pass


class RoundedSpinner(Spinner):
    option_cls = RoundedSpinnerOption
