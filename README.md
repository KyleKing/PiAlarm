# PiAlarm
> Raspberry Pi-powered smart alarm clock. A RGB Light Strip, loud buzzer, bed shaker, web app, geo-location knowledge, and Character LCD display

## The alarm

I'm a heavy sleeper, so I designed the alarm clock to go from pleasant to effective. When the alarm starts, a RGB LED strip lights up and gently increases in brightness. The second stage starts a buzzer and increase the LED strips brightness. The third stage initiates the bed shaker, buzzer, and fades the RGB LED strip between color values at full brightness. At any point, I can press the push button button and turn off the alarm.

<p align="center">
  <img width="550" height=auto src="./README/cover.jpg" alt="above view">
</p>
<p align="center">The prototype alarm</p>

## Display

The current display is a simple character LCD that I had lying around. I'm working on replacing it with a 4 custom RGB LED digits. I'm using shift registers to control the insane number of pins necessary to set each LED individually. I'll update the progress on the new display sometime soon.

## Location Smarts

Using If This Then That (IFTTT), I setup a recipe that makes a web request when I'm away to turn off the alarm and when I return to activate the alarm. This way, the alarm won't run unless I'm present.

## Web app

Using react and socket.io, I built a simple web app accessible anywhere. Once in the app, new alarms can be set using basic cron syntax. The back end of the app handles scheduling, starting, and deleting alarms as I modify the database of alarms.

<p align="center">
  <img width="550" height=auto src="./README/webapp.png" alt="web app">
</p>
<p align="center">The web app</p>

## How to run your own version

<!-- FIXME -->

*(TODO) I'm currently in the midst of revamping the clock display and refactoring the app, so I'll add a guide upon request. Open an issue to let me know that you're interested!*

## Acknowledgments

[Web app based on React example apps published by Twilio](https://www.twilio.com/blog/2015/08/setting-up-react-for-es6-with-webpack-and-babel-2.html)

## Made by

[Kyle King](http://kyleking.me)

<!--

### TODO

> Long Term
- Use heat shrink tubing to better organize the wires with masking tape labels
- Add a plastic surface that presses the button like in my old alarm clock
- *Add the second light strip!
- Figure out what do to with the final housing
....
- Add a sleep button to allow the alarm to be turned off for an hour when I'm up before the first alarm > just one alarm per day
- Setup the dip switch to toggle between regular boot or with the alarm clock > too much work for little reward
- Use the spade connectors with matching gauge wire, find the seam on the spade terminal (usually top), and place seam up to crimp
    > https://www.youtube.com/watch?v=eg9hjqkJWmg
- Cut perf by etching a box cutter fix times along a line of holes. Then snap. Sand as needed, but fiberglass is dangerous to sand FYI
- Setup strain relief on the lead wires

-->
