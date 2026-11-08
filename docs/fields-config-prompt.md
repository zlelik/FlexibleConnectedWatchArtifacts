# What I want

Eight fields down the middle of the screen, from the top: the battery percentage, the date as weekday, day, month and year, the time in the largest font the watch has, steps against the daily goal behind a step icon, sunrise and sunset side by side with their own icons, the next three hourly temperatures behind a thermometer, and today's and tomorrow's forecast high behind an icon chosen by the weather.

Centre every field horizontally and vertically, and write each position in percent rather than pixels so that the layout works on any screen. Name a system font for every field rather than a vector font.

The background picture changes with the sun, so colour the text black in daylight and light blue at night. Colour the battery by charge instead: dark green above 20 percent in daylight, green above 20, orange above 10 and red below that.

# Reference

### 2.8 Fields config

The text fields the watch face draws. Grammar in section 5.

Default:

```
[f1]src=batt;pos=50.0,7.0;just=center|vcenter;frmt=$1$%;nfrmt=%d;colorif=batt>20&isDay=1:0x005500,batt>20:green,batt>10:orange,*:red;sysfont=FONT_TINY;
[f2]src=dayOfWNm,day,monthNm,year;pos=50.0,18.0;just=center|vcenter;frmt=$1$ $2$ $3$ $4$;colorif=isDay=1:black,*:0x00aaff;sysfont=FONT_SMALL;
[f3]src=hour,min;pos=50.0,33.0;just=center|vcenter;frmt=$1$:$2$;nfrmt=%02d,%02d;tf=24h;colorif=isDay=1:black,*:0x00aaff;sysfont=FONT_NUMBER_HOT;
[f4]src=url;pos=50.0,46.0;just=center|vcenter;url=https://myserver.com/r2j.php?url=https://feeds.bbci.co.uk/news/rss.xml&count=1;jsonsrc=items.0.title;frmt=$1$;trunc=25;colorif=isDay=1:black,*:0x00aaff;sysfont=FONT_TINY;
[f5]src=steps,stepGoal;icon=steps;pos=50.0,55.5;just=center|vcenter;frmt=$1$/$2$;colorif=isDay=1:black,*:0x00aaff;sysfont=FONT_MEDIUM;
[f6]src=sunrHour,sunrMin;pos=33.3,65.0;icon=sunrise;just=center|vcenter;frmt=$1$:$2$;nfrmt=%02d;colorif=isDay=1:black,*:0x00aaff;sysfont=FONT_TINY;
[f7]src=sunsHour,sunsMin;pos=66.6,65.0;icon=sunset;just=center|vcenter;frmt=$1$:$2$;nfrmt=%02d;colorif=isDay=1:black,*:0x00aaff;sysfont=FONT_TINY;
[f8]src=wHTemp,wHTemp[1],wHTemp[2];icon=temp;pos=35.0,75.0;just=left|vcenter;frmt=$1$/$2$/$3$;nfrmt=%d;noval=--;colorif=isDay=1:white,*:0x00aaff;sysfont=FONT_TINY;
[f9]src=wDTempHi,wDTempHi[1];pos=35.0,84.0;just=left|vcenter;iconif=wCondS=0:sun,wCondS=1:sunCld,wCondS=2:cld,wCondS=3:rain,wCondS=4:snow,wCondS=5:storm,wCondS=6:fog,wCondS=7:wind,*:qst;frmt=$1$/$2$;nfrmt=%d;noval=--;colorif=isDay=1:white,*:0x00aaff;sysfont=FONT_TINY;
[f10]src=url;icon=btc;iconcolorif=*:orange;pos=50.0,93.0;just=center|vcenter;url=https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd;jsonsrc=bitcoin.usd;frmt=$1$;nfrmt=%d;colorif=isDay=1:white,*:0x00aaff;sysfont=FONT_SMALL;
```

It is shown here one field to a line so that it can be read. The setting itself is one line, with no line break between the fields.

Ten fields down the middle of the screen: the battery, the date, the time in the largest font the watch has, a BBC headline, steps against the daily goal, sunrise and sunset side by side, the next three hourly temperatures, today's and tomorrow's forecast high behind the condition icon, and the bitcoin price. Eight read the watch itself; the headline and the price are fetched from the web.

Six fields carry an **icon** in place of a text label. `f9` is the only one that chooses its icon by rule rather than by name: its `iconif` covers every weather condition in nine rules by naming the condition groups of `wCondS`, and it is the worked example of section 5.10.3. The time has no icon on purpose: at `FONT_NUMBER_HOT` it is the one field nothing should compete with.

Three choices in it make the default work on as many watches as possible. Every field names a **system font** with `sysfont` rather than a vector font, because two of the 39 supported watches have no vector font at all, and on those a field naming only a vector font is drawn in `FONT_SMALL`. Every position is a **percentage**, so the layout scales from a 218 pixel screen to a 466 pixel one without a second config. And every field is drawn `vcenter`, which makes the y percentage the middle of the text rather than its top, so a watch whose system fonts are taller does not push the lower fields off the screen.

Nine of the ten fields colour their text by the time of day, which keeps it readable when the background picture changes with the sun. The six upper ones write `colorif=isDay=1:black,*:0x00aaff`: black over the light sky of the day picture, light blue on the dark night picture. The three lowest sit over the dark water at the bottom of the day picture and write `colorif=isDay=1:white,*:0x00aaff`, the same rule with white in place of black. The battery is the tenth and colours by charge, with the day as a second condition on its first rule. A single `color` cannot do any of this, because the background changes by rule too.

The headline field reads a news feed through a converter. A news feed is RSS, which is XML and far too large for the watch, so the converter fetches the feed and answers with a little JSON: the converter's address is the value of `url`, and the feed's address is a parameter inside it. Only the first `=` of a pair splits it, so `url=https://myserver.com/r2j.php?url=https://feeds.bbci.co.uk/news/rss.xml&count=1` arrives whole. `jsonsrc=items.0.title` reads three steps into the answer, the middle step being a list index. `trunc=25` cuts the finished text to 25 characters, so a long headline stops before the edge of the screen.

Two more details. The battery colour comes from `colorif`, which carries a rule list written exactly as the `BgRules` setting writes one, and its first rule `batt>20&isDay=1:0x005500` is the only rule in the default that names two conditions. And the forecast field asks `wDTempHi` for two different days through the index on each name.

## 4. Background image rules

A rule list chooses one thing out of several by testing what the watch reads. The `BgRules` setting uses one to choose the background picture by its image index. A field of the fields config uses the same grammar in four keys, with something else after the `:`: a colour in `colorif` and `iconcolorif`, an icon name in `iconif`, and nothing at all in `vis`, which takes the conditions alone.

### 4.1 Grammar

```
config    := rule (',' rule)*
rule      := conditions ':' imageIndex
conditions:= '*' | condition ('&' condition)*
condition := metric ('[' index ']')? op number
op        := '<' | '<=' | '>' | '>=' | '=' | '!='
index     := '-'? digit+
```

A comma separates the rules and `&` joins the conditions of one rule. Spaces are ignored. `imageIndex` is a whole number counting from 0. A metric is one of the names of section 4.3, written exactly, upper and lower case included.

Some rule lists for `BgRules`:

| Rule list | Background |
|---|---|
| `isDay=0:1,*:0` | image 1 while the sun is down, image 0 otherwise |
| `batt<15:2,isDay=0:1,*:0` | image 2 while the battery is below 15%, otherwise night or day as above |
| `hr>100&isSleep=0:3,*:0` | image 3 while the heart rate is above 100 and the watch is not in sleep mode |
| `wCondS=3:2,wCondS=4:3,*:0` | image 2 while it rains, image 3 while it snows, image 0 otherwise |
| `minOfDay>=1320:1,minOfDay<420:1,*:0` | image 1 from 22:00 to 07:00, image 0 the rest of the day |

### 4.2 Semantics

**A condition compares one metric against one number, and is therefore either true or false.** `hr>80` is true when the current heart rate is above 80, and false otherwise.

**A rule matches when every condition in it is true.** The conditions are joined with `&`, so `hr>80&stepsPct<50` matches only when the heart rate is above 80 *and* the step percentage is below 50. If either comparison is false, the rule does not match.

**Rules are evaluated in the order written, and the first rule that matches decides the image index.** Evaluation stops at that rule; the rules below it are never evaluated. A rule is therefore only reached when no earlier rule matched, which is what lets bands be written as upper bounds instead of ranges: `batt<10:3,batt<30:2,*:0` is image 3 below 10%, image 2 from 10% to 30% and image 0 above.

`*` is the catch-all. It contains no conditions and always matches, so it belongs last. If no rule matches, which can only happen when the list contains no `*`, image index 0 is used.

`|` (OR) and parentheses are not supported. An OR is written as one rule per branch, all pointing at the same image index and placed next to each other, as the 22:00 to 07:00 example of section 4.1 does. Any rule written between the branches that also matches would be reached first, and the later branch would then never be evaluated.

A metric the watch cannot supply at that moment has no value. **Any condition on a metric with no value is false, whatever the operator**, so with no heart rate reading `hr>80`, `hr<80` and `hr!=80` are all false and the rule does not match. This is not an error.

### 4.3 Metrics

A metric is one reading of the watch, named by a short identifier of letters and digits that starts with a lower case letter. The same names are written in rules and in a field's `src`. Here is every one of them, by group. A value is a whole number unless the table says **decimal**, which can have a fraction, or **whole or decimal**, which can arrive as either, or **text** for the few that are words.

**Time and date.** Always available.

| Metric | Meaning | Value |
|---|---|---|
| `hour` | Hour of the local day | 0 to 23 |
| `min` | Minute of the hour | 0 to 59 |
| `sec` | Second of the minute | 0 to 59. The watch face is redrawn once a minute while the wearer is not looking at it, so a field rarely shows this changing |
| `minOfDay` | Minute of the local day, for a threshold finer than an hour | 0 to 1439. `minOfDay<450` is before 07:30 |
| `dayOfW` | Day of the week | 1 to 7, where 1 is Sunday |
| `dayOfWNm` | Day of the week as a word | `Mon`, `Tue` and so on, in the watch's language. Text |
| `day` | Day of the month | 1 to 31 |
| `month` | Month | 1 to 12 |
| `monthNm` | Month as a word | `Jan`, `Feb` and so on, in the watch's language. Text |
| `year` | Year | for example 2026 |
| `dayOfY` | Day of the year | 1 to 366 |
| `weekOfY` | ISO week number | 1 to 53 |
| `dstOff` | Daylight saving offset | seconds |
| `utcOff` | Offset of the watch's time from UTC | seconds |
| `is24h` | Whether the watch is set to a 24 hour clock | 1 or 0 |

**Sun.** Worked out for the watch's position: the last GPS position the watch knows, or until it knows one, the position typed into the watch face's settings, which is The Hague unless changed.

| Metric | Meaning | Value |
|---|---|---|
| `sunrise` | Sunrise | minutes after local midnight, 0 to 1439. No value on a day the sun does not rise |
| `sunset` | Sunset | minutes after local midnight. No value on a day the sun does not set |
| `isDay` | Whether the sun is up now | 1 or 0. Inside a polar circle, on a day with no sunrise or sunset, 1 from April to September in the north and from October to March in the south |
| `minToSunr` | Minutes until the next sunrise, today's while it is still to come and tomorrow's after it | minutes, never negative |
| `minToSuns` | Minutes until the next sunset, the same way | minutes, never negative |
| `dayLen` | Length of the day from sunrise to sunset | minutes |
| `sunrHour` | Hour of sunrise | 0 to 23 |
| `sunrMin` | Minute of sunrise | 0 to 59 |
| `sunsHour` | Hour of sunset | 0 to 23 |
| `sunsMin` | Minute of sunset | 0 to 59 |

**Position.**

| Metric | Meaning | Value |
|---|---|---|
| `lat` | Latitude the sun is worked out for | degrees, north positive. Decimal |
| `lon` | Longitude the sun is worked out for | degrees, east positive. Decimal |
| `gpsAcc` | Quality of the GPS position the watch knows | 0 to 4: 0 none, 1 last known, 2 poor, 3 usable, 4 good |

**Activity.** From the watch's own activity tracking, counted from local midnight unless the meaning says a week.

| Metric | Meaning | Value |
|---|---|---|
| `steps` | Steps today | count |
| `stepGoal` | Daily step goal | count |
| `stepsPct` | Steps as a percentage of the goal | percent, which passes 100 once the goal is met. No value when the goal is 0 |
| `cal` | Calories today | kcal |
| `dist` | Distance today | metres |
| `floorsUp` | Floors climbed today | count. No value on a watch without a barometer |
| `floorsDn` | Floors descended today | count. No value on a watch without a barometer |
| `floorGoal` | Daily goal of floors climbed | count |
| `floorsPct` | Floors climbed as a percentage of the goal | percent. No value when the goal is 0 |
| `mClimb` | Metres climbed today | metres. Decimal |
| `mDesc` | Metres descended today | metres. Decimal |
| `moveBar` | Move bar level, which rises while the wearer sits still | 0 to 5 |
| `actMinD` | Active minutes today | minutes |
| `actMinDMod` | Moderate active minutes today | minutes |
| `actMinDVig` | Vigorous active minutes today | minutes |
| `actMinW` | Active minutes this week | minutes |
| `actMinWGoal` | Weekly goal of active minutes | minutes |
| `actMinWPct` | Active minutes this week as a percentage of the goal | percent. No value when the goal is 0 |
| `isSleep` | Whether the watch is in sleep mode | 1 or 0 |
| `recovery` | Recovery time left after training | hours |

**Health.**

| Metric | Meaning | Value |
|---|---|---|
| `respRate` | Respiration rate | breaths per minute |
| `stress` | Stress score | 0 to 100 |
| `hr` | Heart rate now | beats per minute. Often no value while the wearer is not looking at the watch |
| `hrMin` | Lowest heart rate in the last hour | beats per minute |
| `hrMax` | Highest heart rate in the last hour | beats per minute |
| `hrRest` | Resting heart rate | beats per minute |
| `hrRestAvg` | Resting heart rate, seven day average | beats per minute |
| `o2` | Blood oxygen saturation | percent. Usually no value, because the watch measures it rarely |
| `vo2Run` | VO2 max for running | ml/kg/min |
| `vo2Bike` | VO2 max for cycling | ml/kg/min |

**Battery and device.**

| Metric | Meaning | Value |
|---|---|---|
| `batt` | Battery left | 0 to 100 percent. Decimal |
| `battDays` | Battery left | days. Decimal |
| `isChrg` | Whether the watch is charging | 1 or 0 |
| `solar` | Solar intensity | 0 to 100 percent. No value on a watch without solar charging |
| `alarms` | Alarms set | count |
| `notifs` | Unread notifications | count |
| `isPhone` | Whether the phone is connected | 1 or 0 |
| `isConn` | Whether any connection is available | 1 or 0 |
| `isDnd` | Whether Do Not Disturb is on | 1 or 0 |
| `isTones` | Whether tones are on | 1 or 0 |
| `isVibr` | Whether vibration is on | 1 or 0 |

**Weather now.** From the weather the phone last sent to the watch, so none of these has a value until the phone has synced.

| Metric | Meaning | Value |
|---|---|---|
| `wTemp` | Temperature | degrees, in the watch's own unit. Whole or decimal |
| `wFeels` | Feels-like temperature | degrees. Decimal |
| `wTempHi` | Today's forecast high | degrees. Whole or decimal |
| `wTempLo` | Today's forecast low | degrees. Whole or decimal |
| `wHumid` | Relative humidity | 0 to 100 percent |
| `wWind` | Wind speed | metres per second. Decimal |
| `wWindDir` | Direction the wind comes from | 0 to 359 degrees |
| `wPrecip` | Chance of precipitation | 0 to 100 percent |
| `wCond` | Weather condition | a code from 0 to 53, below |
| `wCondNm` | Weather condition as a word | `Clear`, `Cloudy`, `Rain`, `Snow`, `Storm`, `Fog`, `Wind` or `Unknown`. Text |
| `wCondS` | Weather condition as a group | 0 to 8, below |
| `wCloud` | Cloud cover | 0 to 100 percent |
| `wUv` | UV index | Decimal |
| `wPress` | Air pressure reported with the weather | pascals. Decimal |
| `wDew` | Dew point | degrees. Decimal |
| `wVis` | Visibility | metres. Decimal |
| `wAge` | Age of the weather reading | minutes |

**Weather by the hour.** Each takes an index, `[n]`, counting hours from the start of the hourly forecast the phone last sent: `wHTemp` is its first hour, `wHTemp[1]` the hour after, `wHTemp[3]` three hours on. Past the end of the forecast there is no value.

| Metric | Meaning | Value |
|---|---|---|
| `wHTemp` | Temperature | degrees. Whole or decimal |
| `wHPrecip` | Chance of precipitation | 0 to 100 percent |
| `wHCond` | Weather condition | a code from 0 to 53, below |
| `wHCondNm` | Weather condition as a word | the words of `wCondNm`. Text |
| `wHCondS` | Weather condition as a group | 0 to 8, below |
| `wHHumid` | Relative humidity | 0 to 100 percent |
| `wHCloud` | Cloud cover | 0 to 100 percent |
| `wHDew` | Dew point | degrees. Decimal |
| `wHUv` | UV index | Decimal |
| `wHWind` | Wind speed | metres per second. Decimal |
| `wHWindDir` | Direction the wind comes from | 0 to 359 degrees |

**Weather by the day.** Each takes an index, `[n]`, counting days: `wDTempHi` is today's, `wDTempHi[1]` tomorrow's. Past the end of the forecast there is no value.

| Metric | Meaning | Value |
|---|---|---|
| `wDTempHi` | Forecast high | degrees. Whole or decimal |
| `wDTempLo` | Forecast low | degrees. Whole or decimal |
| `wDPrecip` | Chance of precipitation | 0 to 100 percent |
| `wDCond` | Weather condition | a code from 0 to 53, below |
| `wDCondNm` | Weather condition as a word | the words of `wCondNm`. Text |
| `wDCondS` | Weather condition as a group | 0 to 8, below |

**Environment.** From the watch's own sensors.

| Metric | Meaning | Value |
|---|---|---|
| `alt` | Altitude | metres. Decimal |
| `press` | Air pressure at the watch | pascals. Decimal |
| `pressMsl` | Air pressure reduced to sea level | pascals. Decimal |
| `heading` | Compass heading | 0 to 359 degrees |

**From the web.**

| Metric | Meaning | Value |
|---|---|---|
| `url` | A value a field with `src=url` fetched | whatever the JSON answer contains at that field's `jsonsrc`. No value until the first fetch has succeeded |

In a field, `src=url` draws the field's own fetched value. In a rule, `url[n]` reads the value fetched by a field of the `FieldsConfig` setting, counting its fields from 0, so `url[9]>70000` tests what the tenth field fetched. It can be compared only when that value is a number.

**Indexed metrics.** The sun metrics `sunrise`, `sunset`, `dayLen`, `sunrHour`, `sunrMin`, `sunsHour` and `sunsMin` take a day index: `sunrise[-1]` is yesterday's, `sunrise[1]` tomorrow's. The hourly and daily weather metrics take the indexes their tables give. A plain name means index 0, and an index on any other metric is accepted and ignored.

**Text metrics cannot be compared.** `dayOfWNm`, `monthNm`, `wCondNm`, `wHCondNm` and `wDCondNm` are words, and `<` means nothing for a word, so a rule naming one is dropped exactly as a rule naming an unknown metric is. A field draws them like any other value. For a rule, use the number beside each: `dayOfW`, `month`, `wCond` or `wCondS`.

**Temperature is in the watch's own unit.** Every temperature metric is in degrees Celsius, or in Fahrenheit when the watch is set to statute units, and a rule's threshold is in the same unit: `wTemp<-3` means −3 °F on a watch set to Fahrenheit. The watch's own unit setting decides, and the watch face has no setting of its own for it. Every other unit is fixed whatever the watch is set to: wind in metres per second, pressure in pascals, distance, altitude and visibility in metres.

**Thresholds may be fractional.** `batt<12.5` and `wTemp<-3` both work.

#### Weather conditions

`wCond`, `wHCond` and `wDCond` are Garmin's condition codes:

0 clear, 1 partly cloudy, 2 mostly cloudy, 3 rain, 4 snow, 5 windy, 6 thunderstorms, 7 wintry mix, 8 fog, 9 hazy, 10 hail, 11 scattered showers, 12 scattered thunderstorms, 13 unknown precipitation, 14 light rain, 15 heavy rain, 16 light snow, 17 heavy snow, 18 light rain and snow, 19 heavy rain and snow, 20 cloudy, 21 rain and snow, 22 partly clear, 23 mostly clear, 24 light showers, 25 showers, 26 heavy showers, 27 chance of showers, 28 chance of thunderstorms, 29 mist, 30 dust, 31 drizzle, 32 tornado, 33 smoke, 34 ice, 35 sand, 36 squall, 37 sandstorm, 38 volcanic ash, 39 haze, 40 fair, 41 hurricane, 42 tropical storm, 43 chance of snow, 44 chance of rain and snow, 45 cloudy with a chance of rain, 46 cloudy with a chance of snow, 47 cloudy with a chance of rain and snow, 48 flurries, 49 freezing rain, 50 sleet, 51 ice and snow, 52 thin clouds, 53 unknown.

**`wCondS`, `wHCondS` and `wDCondS` carry the same reading collapsed to nine groups**, so a rule can name what the weather is doing rather than which of 54 codes it is. Prefer them in a rule: `wCondS=3` is every kind of rain in one condition.

| Value | Group | Codes |
|---|---|---|
| 0 | clear sky | 0, 23, 40 |
| 1 | some cloud, sun behind it | 1, 22 |
| 2 | mostly or wholly cloudy | 2, 20, 52 |
| 3 | rain, including tornado, hurricane, tropical storm and freezing rain | 3, 11, 13 to 15, 24 to 27, 31, 32, 41, 42, 45, 49 |
| 4 | snow, including every mixture of snow and rain | 4, 7, 10, 16 to 19, 21, 34, 43, 44, 46 to 48, 50, 51 |
| 5 | thunder and squall | 6, 12, 28, 36 |
| 6 | fog and the other obscurations: mist, haze, smoke, volcanic ash | 8, 9, 29, 33, 38, 39 |
| 7 | wind and blown dust or sand | 5, 30, 35, 37 |
| 8 | a code no group covers | anything else, 53 included |

`wCondNm` and its hourly and daily forms name the same groups in words, one group coarser: groups 1 and 2 are both `Cloudy`, and group 8 is `Unknown`.

### 4.3.1 Rules compare a metric against a number

Never against another metric. There is no way to write `minOfDay>sunrise`, which is why `isDay` exists as a metric of its own: it is that comparison, already made. Any rule about whether the sun is up should use it.

### 4.4 Malformed rules

A rule that does not parse is dropped and the remaining rules still work, so one typo cannot leave the watch face with no rules at all. A rule naming a metric that does not exist, comparing a text metric, or comparing against something that is not a number is dropped the same way, without any message.

## 5. Fields config

The `FieldsConfig` setting describes every text field the watch face draws, in one line of text: what each field shows, where it goes, how its value is written, and in which font and colour, with which icon. Section 2.8 has the default, a complete example.

### 5.1 Grammar

```
config := field*
field  := '[' label ']' pair*
pair   := key '=' value ';'
```

The `[label]` opens a field. **The label text is ignored**: a field is numbered by its position in the config, so duplicate or out-of-order labels are harmless. Labels such as `[f1]`, `[f2]` keep a config readable.

A pair splits on its **first** `=` only, because values contain `=` — a query string such as `?ids=bitcoin&vs_currencies=usd` must survive intact.

**The whole config is one line**, and every pair ends with `;`, the last one included. A field opens only where a `[` starts the config or comes straight after a `;`. A line break or a space in front of a `[` therefore stops that field opening: the watch applies its keys to the field before it, and says nothing.

### 5.2 Escaping

A value ends at the first `;`. The config has escapes for the two characters that would otherwise be impossible in a value, `\;` for a semicolon and `\\` for a backslash, but **never write either**. The Connect IQ settings editor on the phone cannot save a value that contains `\;`: it answers `Unable to contact server error 500`, and the whole settings screen stops working until the value is changed by other means. Write `:` or `-` where a semicolon was wanted.

`<` and `>` are written as they are, as in `colorif=batt>20:green`. The settings editor stores the text exactly as typed.

### 5.3 Keys

| Key | Applies to | Meaning |
|---|---|---|
| `src` | all | What the field shows: one or more metrics, `url` or `str`. Section 5.4. Required. |
| `pos` | all | Where the field is, `x,y`, each a percentage of the screen unless it says `px`. Section 5.8. Required. |
| `color` | all | Text colour, a colour name or `0xRRGGBB` of section 6. Without it the text is drawn in the watch face's foreground colour setting, which is black unless changed. |
| `colorif` | all | Text colour by rule, in the grammar of section 4, with a colour where the image index goes: `batt>20:green,batt>10:orange,*:red`. The first match wins, and no match leaves `color` to decide. |
| `frmt` | all | The text template, in which `$1$` is the first value: `frmt=$1$:$2$`. The only place static text goes: a label, a unit or both. Section 5.5. Without it the field draws its first value alone. |
| `nfrmt` | numbers | How each number is written, such as `%02d` or `%.1f`, one per value and comma separated, or one for every value. Section 5.5. Without it a number is written plainly. |
| `mul` | numbers | A multiplier for each value before it is written, one per value or one for every value: `mul=0.001` turns metres into kilometres. Section 5.5. |
| `tf` | `hour`, `sunrHour`, `sunsHour` | `24h` or `12h`. With `12h` the hour is written 1 to 12, with no AM or PM. Defaults to `24h`. |
| `trunc` | all | The most characters the finished text may have, counting every part of it including any label in `frmt`. |
| `noval` | all | Text drawn in place of a value the watch cannot supply: `noval=--`. Without it such a value is drawn as nothing. |
| `sysfont` | all | A system font by name, section 5.6.2. The one way to choose a font that works on every watch. |
| `font` | all | A vector font and its size in pixels, `font=#RobotoCondensedBold:20`, section 5.6.1. Used when the watch has that font, and otherwise the field is drawn in its `sysfont`, or in `FONT_SMALL` when it names none. |
| `just` | all | Alignment: `left`, `center` or `right` for x, and `vcenter` for y. Section 5.7, which shows how they are joined. Defaults to `left`, with y at the top of the text. |
| `vis` | all | Conditions in the grammar of section 4.1, joined by `&`, with no `:` and no comma: `vis=isPhone=1`. The field is drawn only while they are all true. A condition that does not parse leaves the field visible. |
| `url` | `src=url` | The address to fetch. Required for `src=url`. |
| `jsonsrc` | `src=url` | Where the value is in the JSON answer, as a dotted path such as `bitcoin.usd` or `items.0.title`. Section 5.4. Required for `src=url`. |
| `icon` | all | An icon by name, as in `icon=sunrise`. Section 5.10. |
| `iconif` | all | Icon by rule, in the grammar of section 4, with an icon name where the image index goes: `wCondS=3:rain,*:sun`. The first match wins and beats `icon`; no match leaves `icon` to decide. |
| `iconcolorif` | all | Colour the icon by rule, the same grammar as `colorif`. Without it the icon takes whatever colour the text is drawn in. |
| `iconpos` | all | `left` or `right`, which side of the text the icon goes. Defaults to `left`. |

A key is written exactly as in this table, in lower case. **A key that is not in the table is ignored without any message**, so a misspelt key silently does nothing. When a field carries the same key twice, the later one counts.

### 5.4 Sources

`src` names what the field shows:

| `src` | What the field shows |
|---|---|
| A metric of section 4.3 | its value |
| Several metrics, comma separated, as in `src=steps,stepGoal` | one value per metric, in the order written, which `frmt` places as `$1$`, `$2$` and so on |
| `url` | one value read out of the JSON a web address answers with |
| `str` | no value at all. The field draws its `frmt` and nothing else, which is how static text gets onto the watch face: `src=str;frmt=JOHN'S WATCH;` |

Every metric takes the optional `[index]` of section 4.3: `src=batt`, `src=steps,stepGoal`, `src=sunrise[1]`, `src=wDTempHi,wDTempHi[1]`. A name that is not a metric drops the whole field, so a typo is visible rather than silently drawing the wrong reading.

A value the watch cannot supply is empty in its own place rather than cancelling the field, so `src=wTemp,wDTempHi[1]` still draws the reading it has when the other is missing. A field draws whatever its finished text comes to and nothing more, and draws nothing only when that finished text is empty. A missing value and an empty text are the same thing here, since a web answer can carry either for something it does not have, while `0` is a value and is written `0`. So with `frmt=Pref: $1$` the three draw `Pref: `, `Pref: ` and `Pref: 0`, and with `frmt=$1$` they draw nothing, nothing and `0`.

`noval` puts text in the place of a value there is none of, which is how a field says `--` rather than leaving a gap in its template. It covers both forms: `noval=--` with `frmt=Pref: $1$` draws `Pref: --` whether the value was missing or empty, and still draws `Pref: 0` for a zero.

**`src=url` fetches a value from the web.** The watch fetches the address in `url` about every five minutes, keeps the last value it read, and keeps it when a fetch fails, so the field shows nothing only until the first fetch succeeds. The answer has to be JSON, and small: the watch reads it in a small amount of memory, so a large answer, such as a whole news feed, is not read at all. `jsonsrc` is a dotted path into it: `jsonsrc=bitcoin.usd` reads `77590` out of `{"bitcoin":{"usd":77590}}`. A step that is a whole number indexes a list instead of an object, so `items.0.title` reads the first headline of `{"items":[{"title":...}]}` and `items.-1.title` the last.

### 5.5 Formatting

Each value of a field goes through three steps, in this order: `mul` multiplies it, `nfrmt` writes it as text, and `frmt` places it in the template. `trunc` then cuts the finished text.

**`nfrmt`** carries one specifier per value, comma separated, each written `%[flags][width][.precision]specifier` as in C's `printf`:

```
nfrmt=%02d,%02d
```

| Specifier | Writes |
|---|---|
| `d` or `i` | a whole number, the fraction cut off rather than rounded: 76.5 is written `76` |
| `u` | a whole number without a sign |
| `f` | a decimal number, six places unless the precision says otherwise: `%.1f` writes 76.5 as `76.5` and 12 as `12.0` |
| `e`, `E` | scientific notation, with a small or a capital E |
| `x`, `X`, `o` | hexadecimal in small or capital letters, and octal |

The two flags are `0`, which pads to the width with zeros, so `%02d` writes 8 as `08`, and `+`, which writes a sign on positive numbers as well. Width and precision are plain numbers.

A single specifier applies to every value, so six values padded the same way is `nfrmt=%02d` rather than the specifier written six times. An empty position leaves that value unformatted, as does a position past the end of the list.

Without `nfrmt` a number is written plainly, and a value that arrives as a decimal is written with at least one decimal: `batt` draws `76.5`, and a temperature of 12 degrees can draw `12.0`. Give a metric section 4.3 marks decimal, or whole or decimal, `nfrmt=%d` or `nfrmt=%.1f`. A value a specifier cannot apply to, such as text, is written as it is.

**`frmt`** carries the text template, in which `$1$` is the first value, `$2$` the second, and so on:

```
frmt=$1$:$2$
```

The template is positional, so a value can be repeated or the order changed, and text between the substitutions is drawn exactly as written. Static text belongs here: there is no separate prefix or suffix key, and `frmt=Steps: $1$/$2$` and `frmt=$1$%` write a label and a unit.

`frmt` is optional. Without it a field draws its first value on its own, which is what a field showing a single value wants:

```
[f1]src=hr;pos=50.0,23.8;nfrmt=%02d;
```

A `$N$` with no value behind it draws as nothing, so `frmt=$1$:$2$:$3$` on a field supplying two values draws `09:05:`. `$0$` names no value and draws the word `null`, which makes that mistake visible on the watch face. A `$` that does not form `$N$` is drawn as it is, so `frmt=price $1$` works, and a value that itself contains `$1$` is drawn as it is rather than substituted again. A value the template does not name is not drawn, so a template naming fewer values than the field supplies simply leaves the rest out.

**`mul`** carries one multiplier per value, comma separated, or one for every value, as `nfrmt` does. A multiplied value is a decimal number, so it wants an `nfrmt` as well: `src=dist;mul=0.001;nfrmt=%.1f;frmt=$1$ km` draws 6321 metres as `6.3 km`. Some useful multipliers:

| From | To | `mul` |
|---|---|---|
| metres | kilometres | `0.001` |
| metres | miles | `0.000621371` |
| metres | feet | `3.28084` |
| metres per second | kilometres per hour | `3.6` |
| metres per second | miles per hour | `2.23694` |
| metres per second | knots | `1.94384` |
| pascals | hectopascals, which are millibars | `0.01` |
| pascals | inches of mercury | `0.0002953` |

A temperature needs no multiplier: it is already in the watch's own unit, section 4.3.

**`trunc`** is the most characters the finished text may have, counting everything in it, the label in `frmt` included: `trunc=25`. An icon is not counted.

**`tf=12h`** writes an hour of the local day 1 to 12, where 0 becomes 12 and 13 becomes 1, with no AM or PM marker. It applies to `hour`, `sunrHour` and `sunsHour` and to nothing else.

### 5.6 Fonts

Two keys choose a font. `sysfont` names one of the nine **system fonts**, which every watch has, at a size the watch decides. `font` names a **vector font** and a size in pixels, and only some watches have a given vector font. A field may carry both: the watch draws the vector font when it has it and the system font otherwise. A field naming neither is drawn in `FONT_SMALL`.

**A field that has to look right on every watch names a `sysfont`.** That is what the default of section 2.8 does for all ten fields.

#### 5.6.1 Vector fonts

`font=#RobotoCondensedBold:20` names the font and its size in pixels; the `#` is optional. The name is written exactly as below, upper and lower case included: `BionicSemiBold` on one watch is spelled `BionicSemibold` on another. A watch that does not have the font draws the field in its `sysfont`, or in `FONT_SMALL` when it names none, without any message.

Four vector fonts are on every one of the 37 supported watches that have vector fonts, and are the ones a config meant for any watch can use. The other two, the Forerunner 255 Music and the Forerunner 255S Music, have no vector font at all.

| Font | On how many of the 39 watches |
|---|---|
| `KosugiRegular`, `NotoSansSCMedium`, `RobotoCondensedBold`, `RobotoCondensedRegular` | 37 |
| `BionicBold` | 28 |
| `NotoNaskhArabicBold`, `NotoNaskhArabicRegular`, `NotoSansArmenianBold`, `NotoSansArmenianRegular`, `NotoSansHebrewBold`, `NotoSansHebrewRegular` | 27 |
| `NanumGothicBold`, `PridiRegular`, `RobotoItalic`, `RobotoRegular` | 23 |
| `BionicMedium`, `RobotoMedium` | 12 |
| `NanumGothicRegular`, `PridiRegularGarmin`, `SakkalMajallaBold`, `SakkalMajallaRoman`, `Swiss721Bold`, `Swiss721Regular` | 10 |
| `NanumGothicExtraBold`, `PridiSemiBoldGarmin`, `RobotoCondensedRegularItalic` | 4 |
| `BionicSemiBold` | 3 |
| `BionicSemibold`, `RobotoBlack` | 1 |

The fēnix 7 and epix 2 Pro watches have eleven: the four, `BionicBold`, and the six of the row of ten. The fēnix 8 and fēnix 9 watches mostly have seventeen, and the newer Forerunners fourteen or fifteen. On the fēnix 7 and epix 2 Pro watches `BionicBold` has digits and no letters.

A font draws only the characters it contains, and it does not borrow a missing one from another font, so a language needs a font that has its script:

| Script | Fonts that have it |
|---|---|
| English | all, except `NotoNaskhArabic`, `NotoSansArmenian`, `NotoSansHebrew` and `SakkalMajalla`, which have no Latin letters |
| Western European accents, such as é and ü | the Roboto, NanumGothic, Pridi and Bionic fonts and `NotoSansSCMedium`. Not `KosugiRegular` or `Swiss721` |
| Central European letters, such as ł and ő | the Roboto, Pridi and Bionic fonts |
| Cyrillic and Greek | the Roboto and NanumGothic fonts, `NotoSansSCMedium` and `KosugiRegular` |
| Chinese | `NotoSansSCMedium`, `KosugiRegular` and the NanumGothic fonts |
| Japanese kana | `KosugiRegular` |
| Korean | the NanumGothic fonts |
| Hebrew | `NotoSansHebrewRegular`, `NotoSansHebrewBold`, `Swiss721Regular`, `Swiss721Bold` |
| Arabic | `NotoNaskhArabicRegular`, `NotoNaskhArabicBold`, `SakkalMajallaRoman`, `SakkalMajallaBold` |
| Armenian | `NotoSansArmenianRegular`, `NotoSansArmenianBold` |
| Thai | the Pridi fonts |

#### 5.6.2 System fonts

`sysfont` takes one of nine names, and every watch has all nine:

| `sysfont` | For | Height of its digits, in percent of the screen height |
|---|---|---|
| `FONT_XTINY` | text | 4 to 5 |
| `FONT_TINY` | text | 6 to 7 |
| `FONT_SMALL` | text | 7 to 8 |
| `FONT_MEDIUM` | text | 8 to 9 |
| `FONT_LARGE` | text | 9 to 10 |
| `FONT_NUMBER_MILD` | numbers | 9 to 15 |
| `FONT_NUMBER_MEDIUM` | numbers | 11 to 18 |
| `FONT_NUMBER_HOT` | numbers | 18 to 21 |
| `FONT_NUMBER_THAI_HOT` | numbers | 20 to 24 |

Each watch decides the size of each of them, which is why the heights are ranges: they were measured across the 39 supported watches, and a small screen gets relatively larger text. On a 260 pixel fēnix 7 the digits of `FONT_TINY` are 17 pixels tall, of `FONT_SMALL` 19, of `FONT_MEDIUM` 22 and of `FONT_NUMBER_HOT` 50. A line of text takes about 1.4 times the height of its digits, for the letters that reach above and below them, so two fields one above the other want their `y` at least that far apart.

**The four number fonts are for numbers.** On the fēnix 7, epix 2 Pro and Forerunner 255 Music watches they contain the digits, the space and `# % + - . / :` and nothing else, so a word in a field drawn with one goes missing there. Keep words in a text font: the time is `FONT_NUMBER_HOT` and its label, if any, is a field of its own.

Every name has the `FONT_` prefix and is written in capitals; a name that is not one of the nine leaves the field in `FONT_SMALL`.

The wearer can make the system fonts larger in the watch's own settings, with a font size setting or a high readability mode, and every field drawn in a system font then grows with them. A layout that only just fits leaves no room for that.

#### 5.6.3 Which characters a font can draw

**No emoji can be drawn, on any watch, in any font.** No font on any of the watches contains a character above `U+FFFF`, so an emoji draws as an empty rectangle whatever the config says. The icons of section 5.10 are the way to put a picture beside a value.

**A system font draws Latin-1**: the letters of the Western European languages, digits and common punctuation. Some watches' system fonts carry more, Cyrillic among them, but not every watch's, so text in another script needs a vector font with that script, section 5.6.1.

**Symbols below `U+FFFF` work in a vector font that contains them.** `NotoSansSCMedium`, which every watch with vector fonts has, contains these: `☀ ☁ ☂ ☃`, the arrows `← ↑ → ↓ ⬆ ⬇`, the shapes `■ □ ▲ ▼ ● ○ ◆ ★ ☆`, the blocks `█ ▓ ▒ ░`, `♥ ♡ ♪ ⚠ ✓ ✂ ➡ ☉`, the units `° ℃ ℉` and the circled numbers `① ② ③`. `✖` is in the NanumGothic fonts only. A field drawing a symbol therefore names `font=#NotoSansSCMedium:<size>`; the same symbol in a system font, or in a vector font without it, draws as an empty rectangle.

Two traps. A character Unicode shows as a colour emoji is missing even below `U+FFFF`, which is why `⚡` `U+26A1`, `☕` `U+2615`, `❄` `U+2744` and `❤` `U+2764` all fail while their plain neighbours work. And a plain and a heavy form are separate characters: `✓` `U+2713` is there and `✔` `U+2714` is not, so the exact character matters rather than one that looks like it.

### 5.7 Justification

`just` is a `|` separated list: one of `left`, `center` and `right` for the horizontal, and `vcenter` for the vertical, in any order and in any case, as in `just=center|vcenter`.

| `just` | x is |
|---|---|
| `left`, the default | the left edge of the field |
| `center` | the middle of the field |
| `right` | the right edge of the field |

| `just` | y is |
|---|---|
| without `vcenter`, the default | the top of the text line |
| with `vcenter` | the middle of the digits, which is the middle of the text for a number |

A field with an icon places the icon and its text together, as one block, section 5.10.1.

### 5.8 Positions

`pos=x,y` places a field. x counts from the left edge of the screen and y from the top. **A coordinate is a percentage of the screen's width or height** unless it says otherwise: `pos=50,25` and `pos=50%,25%` are the same, the middle of the width and a quarter of the way down. `px` makes a coordinate a pixel count from the left or top edge, as in `pos=130px,40px`. The two are read separately, so `pos=50%,10px` is the middle of the width and 10 pixels down. A coordinate may have decimals: `pos=33.3,65.0`.

**Percentages are the way to write one layout for every watch.** The supported screens are 218 to 466 pixels across, so a pixel position written for one is wrong on all the others.

What the point means depends on `just`, section 5.7: with `just=center|vcenter`, which the default uses everywhere, `pos` is the middle of the field.

**Every supported watch has a round screen.** The corners of the square are outside the display, so a field near the top or the bottom has less room the closer it is to the edge, and the part of a field outside the screen is not drawn:

| Distance of a line from the top or bottom edge | Width of the screen there |
|---|---|
| 5% | 44% |
| 10% | 60% |
| 15% | 71% |
| 20% | 80% |
| 30% | 92% |
| 50%, the middle | 100% |

### 5.9 Malformed fields

A field missing `src` or `pos`, naming a metric that does not exist, or with `src=url` but no `url` or no `jsonsrc`, is dropped. The remaining fields still draw.

An unknown key is ignored, and so is a colour that is neither a colour name nor `0xRRGGBB`, which leaves the text in the foreground colour. An unknown icon name, or an `iconif` rule naming one, costs the icon and not the field: the text still draws. A `font` the watch does not have leaves the field in its `sysfont`, or in `FONT_SMALL`. None of these says anything on the watch, so the field simply looks different from what was intended.

### 5.10 Icons

An icon is a small picture drawn beside a field's text, named by `icon`:

```
[f1]src=hr;icon=hr;pos=50%,40%;just=center|vcenter;frmt=$1$ bpm;
```

An icon is drawn on every watch, in the colour of the field's text or in its own through `iconcolorif`. Its size follows the screen: 24 pixels on screens up to 280 pixels across, 31 on 360 to 416 and 38 on 454 and 466, which is about 1.2 times the height of `FONT_SMALL` text. A field carries at most one icon.

These are all the icons. A name is written exactly as below, upper and lower case included.

| Icon | Picture | Meant for |
|---|---|---|
| `clock` | clock | the time: `hour`, `min`, `sec`, `minOfDay` |
| `date` | calendar | the date: `day`, `dayOfW`, `dayOfWNm`, `month`, `monthNm`, `year`, `dayOfY`, `weekOfY` |
| `globe` | globe | the time zone: `utcOff`, `dstOff`, `is24h` |
| `hrGls` | hourglass | a length of time: `minToSunr`, `minToSuns`, `dayLen`, `recovery` |
| `sunrise` | sun rising above a line | sunrise: `sunrise`, `sunrHour`, `sunrMin` |
| `sunset` | sun setting below a line | sunset: `sunset`, `sunsHour`, `sunsMin` |
| `sun` | sun | the sun being up, `isDay`, and a clear sky, `wCondS` group 0 |
| `moon` | crescent moon | night, or Do Not Disturb |
| `moonS` | moon and stars | night |
| `gps` | map pin | position: `lat`, `lon` |
| `gpsAcc` | radio waves | GPS quality: `gpsAcc` |
| `comp` | compass | heading: `heading` |
| `steps` | footprints | steps: `steps`, `stepGoal`, `stepsPct` |
| `fire` | flame | calories: `cal` |
| `dist` | winding path | distance: `dist` |
| `floors` | stairs | floors: `floorsUp`, `floorsDn`, `floorGoal`, `floorsPct` |
| `mClimb` | stairs going up | metres climbed: `mClimb` |
| `mDesc` | stairs going down | metres descended: `mDesc` |
| `move` | moving shoe | the move bar: `moveBar` |
| `actv` | running figure | active minutes: `actMinD`, `actMinDMod`, `actMinDVig`, `actMinW`, `actMinWGoal`, `actMinWPct`, and running VO2 max, `vo2Run` |
| `sleep` | bed | sleep mode: `isSleep` |
| `goal` | target | a goal, beside a value that could be mistaken for a reading |
| `hr` | heart | heart rate: `hr`, `hrMin`, `hrMax` |
| `hrRest` | heart with a pulse line | resting heart rate: `hrRest`, `hrRestAvg` |
| `lung` | lungs | respiration: `respRate` |
| `stress` | nervous smiley | stress: `stress` |
| `o2` | sawtooth wave | blood oxygen: `o2` |
| `user` | person | a person, such as an owner's name in a `str` field |
| `scale` | scales | body weight |
| `ruler` | ruler | body height |
| `bike` | cyclist | cycling VO2 max: `vo2Bike` |
| `batt` | full battery | battery: `batt`, `battDays` |
| `chrg` | battery with a lightning bolt | charging: `isChrg` |
| `solar` | solar panel | solar intensity: `solar` |
| `mem` | memory chip | memory |
| `alrm` | alarm clock | alarms: `alarms` |
| `msg` | envelope | notifications: `notifs` |
| `phone` | mobile phone | the phone connection: `isPhone` |
| `conn` | Bluetooth sign | any connection: `isConn` |
| `dnd` | bell struck through | Do Not Disturb: `isDnd` |
| `bell` | bell | tones: `isTones` |
| `vibr` | vibrating phone | vibration: `isVibr` |
| `temp` | thermometer | temperature: `wTemp`, `wTempHi`, `wTempLo`, `wHTemp`, `wDTempHi`, `wDTempLo` |
| `tmpfeels` | thermometer with heat | feels-like temperature: `wFeels` |
| `humid` | drop | humidity: `wHumid`, `wHHumid` |
| `dew` | half-filled drop | dew point: `wDew`, `wHDew` |
| `wind` | wind lines | wind speed, `wWind` and `wHWind`, and wind, `wCondS` group 7 |
| `wdir` | arrow | wind direction: `wWindDir`, `wHWindDir`. It does not turn with the wind |
| `rain` | cloud with rain | rain, `wCondS` group 3, and the chance of it: `wPrecip`, `wHPrecip`, `wDPrecip` |
| `cld` | cloud | cloud cover, `wCloud` and `wHCloud`, and a cloudy sky, `wCondS` group 2 |
| `sunCld` | sun behind a cloud | some cloud, `wCondS` group 1, and the weather condition in general: `wCond`, `wCondNm` and their hourly and daily forms |
| `snow` | cloud with snow | snow, `wCondS` group 4 |
| `storm` | cloud with lightning | thunder, `wCondS` group 5 |
| `fog` | cloud with fog | fog, `wCondS` group 6 |
| `vis` | eye | visibility: `wVis` |
| `press` | arrows pressing on a line | air pressure: `wPress`, `press`, `pressMsl` |
| `alt` | mountains | altitude: `alt` |
| `news` | newspaper | a value from the web: `src=url` |
| `btc` | bitcoin sign | a bitcoin price, with `src=url` |
| `eth` | ethereum diamond | an ethereum price, with `src=url` |
| `sol` | Solana sign | a Solana price, with `src=url` |
| `qst` | question mark | something unknown, such as a weather condition no group covers |

#### 5.10.1 Where the icon goes

**The field's `just` places the icon and the text together, as one block.** The watch measures both and treats the pair as one piece of text:

| `just` | x is |
|---|---|
| `left` | the left edge of the icon |
| `center` | the middle of the icon, the gap and the text together |
| `right` | the right edge of the text |

The gap between the icon and the text is an eighth of the icon's width, at least 2 pixels. A config never carries a pixel offset for an icon and does not need one.

`iconpos=right` puts the icon after the text instead. Nothing else changes.

**An icon-only field** is one whose finished text is empty, which is how a Bluetooth or alarm indicator is written:

```
[f1]src=str;icon=conn;pos=50%,40%;just=center|vcenter;vis=isConn=1;
```

A field draws when it has either an icon or text, and draws nothing only when it has neither. With no text there is no gap, so a centred icon-only field puts the middle of the icon on x. `frmt` can be left out entirely rather than written empty.

`trunc` counts characters and so does not see the icon: a field carrying one is the icon and the gap wider than its text.

#### 5.10.2 How the icon and the text line up vertically

**Give a field with an icon `vcenter`.** The icon and the text are then both centred on the field's y and line up with each other. Without it both start at y, and since an icon and a line of text are not the same height, they do not line up.

#### 5.10.3 Choosing the icon by rule

`iconif` carries rules in the grammar of section 4, with an icon name where the image index goes, and the first match wins:

```
[f1]src=str;iconif=wCond<=0:sun,wCond<=1:sunCld,wCond<=2:cld,*:qst;pos=50%,50%;
```

When no rule matches, whatever `icon` names is drawn; with neither, the field has no icon. A rule naming an icon that does not exist is dropped.

**The weather is what the key is for.** The nine groups of `wCondS` in section 4.3 each have an icon, so one rule per group gives every one of the 54 weather conditions a picture:

```
iconif=wCondS=0:sun,wCondS=1:sunCld,wCondS=2:cld,wCondS=3:rain,wCondS=4:snow,wCondS=5:storm,wCondS=6:fog,wCondS=7:wind,*:qst;
```

| `wCondS` | Weather | Icon |
|---|---|---|
| 0 | clear sky | `sun` |
| 1 | some cloud, sun behind it | `sunCld` |
| 2 | mostly or wholly cloudy | `cld` |
| 3 | rain, including tornado, hurricane, tropical storm and freezing rain, which are all wet | `rain` |
| 4 | snow, including the mixtures of snow and rain: the question is rain or snow, not how much of each | `snow` |
| 5 | thunder and squall | `storm` |
| 6 | fog, mist, haze, smoke and volcanic ash | `fog` |
| 7 | wind, dust and sand | `wind` |
| 8 | a condition no group covers | `qst`, through the last rule `*:qst` |

The last rule is the question mark rather than any weather, so a condition the watch reports in some later version says it does not know rather than claiming snow. The default config of section 2.8 writes its forecast field this way. For the forecast, `wHCondS[n]` and `wDCondS[n]` take the hours and days of section 4.3.

#### 5.10.4 Colouring the icon

Without `iconcolorif` the icon takes whatever colour the text is drawn in, so a one-coloured field needs no extra key. With it, the icon is coloured by its own rules in the same grammar as `colorif`, which is how a yellow sun draws in front of black text:

```
[f1]src=sunrHour,sunrMin;icon=sunrise;iconcolorif=*:yellow;colorif=isDay=1:black,*:0x00aaff;pos=50%,61%;just=center|vcenter;frmt=$1$:$2$;nfrmt=%02d;
```

### 5.11 How many fields

**The watch draws at most 10 fields**: the first ten in the config that are not dropped under section 5.9. Fields after the tenth are ignored, so a field is lost from the end of the config and never from the middle, and a field that is dropped takes no place among the ten. Ten fields fill a round screen from top to bottom, as the default of section 2.8 shows.

## 6. Colours

A colour is one of these 14 names, in any case, or a `0xRRGGBB` value such as `0x005500` for a dark green:

| Name | Value |
|---|---|
| `white` | `0xFFFFFF` |
| `lt_gray` | `0xAAAAAA` |
| `dk_gray` | `0x555555` |
| `black` | `0x000000` |
| `red` | `0xFF0000` |
| `dk_red` | `0xAA0000` |
| `orange` | `0xFF5500` |
| `yellow` | `0xFFAA00` |
| `green` | `0x00FF00` |
| `dk_green` | `0x00AA00` |
| `blue` | `0x00AAFF` |
| `dk_blue` | `0x0000FF` |
| `purple` | `0xAA00FF` |
| `pink` | `0xFF00FF` |

`blue` is a light blue and `dk_blue` the saturated one. `transparent` is not among them. Some watches show fewer colours than `0xRRGGBB` can name — the fēnix 7 shows 64 — and draw any other value as one of the colours they have; the 14 names are among them on every watch.

# Your answer

Answer with the value of the `FieldsConfig` setting and nothing else: one line, with no code fence, no commentary and no line breaks before or after it.

Write the plain `<` and `>` characters, never `&lt;` or `&gt;`: the settings editor on the phone stores the text as typed and does its own escaping.

Never write `\;`. A literal semicolon inside text is the one thing it would be for, and a config carrying one cannot be edited in the phone settings editor afterwards. Write `:` or `-` instead.
