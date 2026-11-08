# What I want

I have two background pictures. Index 0 is the day picture and index 1 is the night one.

Show the night picture while the sun is down and the day picture while it is up.

# Reference

### 2.5 Background image URLs

The pictures the watch face can draw as its background, as a list of image URLs separated by `;`. Each URL's position in the list is its **image index**, counting from 0, which is what the background image rules select.

Default:

```
https://raw.githubusercontent.com/zlelik/FlexibleConnectedWatchArtifacts/refs/heads/main/imgs/DayBG_260x260.png;https://raw.githubusercontent.com/zlelik/FlexibleConnectedWatchArtifacts/refs/heads/main/imgs/NightBG_260x260.png
```

So index 0 is the day image and index 1 is the night image.

A picture the size of the watch's screen fills it exactly, 260 by 260 pixels on a fēnix 7, and a picture of another size is drawn centred. The watch downloads every picture once and keeps it, and downloads them again only when this list changes. A URL in the list cannot contain a `;`, because the list is cut at every one.

### 2.6 Background image rules

A rule list that selects the image index of section 2.5 to draw. Grammar and semantics are in section 4.

Default:

```
isDay=0:1,*:0
```

Image 1 while the sun is down, image 0 while it is up, following real sunrise and sunset at the watch's position rather than a fixed clock time.

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

# Your answer

Answer with the value of the `BgRules` setting and nothing else: one line, with no code fence, no commentary and no line breaks before or after it.

Write the plain `<` and `>` characters, never `&lt;` or `&gt;`: the settings editor on the phone stores the text as typed and does its own escaping.

Never write `\;`. A literal semicolon inside text is the one thing it would be for, and a config carrying one cannot be edited in the phone settings editor afterwards. Write `:` or `-` instead.
