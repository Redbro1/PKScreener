"""
    The MIT License (MIT)

    Copyright (c) 2023 pkjmesra

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.

"""

from PKDevTools.classes.ColorText import colorText

from pkscreener.classes.Pktalib import pktalib
# from PKDevTools.classes.log import measure_time

class CandlePatterns:
    reversalPatternsBullish = [
        "Morning Star",
        "Morning Doji Star",
        "3 Inside Up",
        "Hammer",
        "3 White Soldiers",
        "Bullish Engulfing",
        "Dragonfly Doji",
        "Supply Drought",
        "Demand Rise",
    ]
    reversalPatternsBearish = [
        "Evening Star",
        "Evening Doji Star",
        "3 Inside Down",
        "Inverted Hammer",
        "Hanging Man",
        "3 Black Crows",
        "Bearish Engulfing",
        "Shooting Star",
        "Gravestone Doji",
    ]

    def __init__(self):
        pass

    def findCurrentSavedValue(self, screenDict, saveDict, key):
        existingScreen = screenDict.get(key)
        existingSave = saveDict.get(key)
        existingScreen = f"{existingScreen}, " if (existingScreen is not None and len(existingScreen) > 0) else ""
        existingSave = f"{existingSave}, " if (existingSave is not None and len(existingSave) > 0) else ""
        return existingScreen, existingSave

    #@measure_time
    # Find candle-stick patterns
    # Arrange if statements with max priority from top to bottom
    def findPattern(self, data, dict, saveDict):
        data = data.head(4)
        data = data[::-1]
        hasCandleStickPattern = False
        if "Pattern" not in saveDict.keys():
            saveDict["Pattern"] = ""
            dict["Pattern"] = ""
        # Only 'doji' and 'inside' is internally implemented by pandas_ta.
        # Otherwise, for the rest of the candle patterns, they also need
        # TA-Lib.
        check = pktalib.CDLDOJI(data["Open"], data["High"], data["Low"], data["Close"])
        if check is not None and check.tail(1).item() != 0:
            dict["Pattern"] = self.findCurrentSavedValue(dict,saveDict,"Pattern")[0] + f"Doji" + colorText.END 
            saveDict["Pattern"] = self.findCurrentSavedValue(dict,saveDict,"Pattern")[1] +  f"Doji"
            hasCandleStickPattern = True

        check = pktalib.CDLMORNINGSTAR(
            data["Open"], data["High"], data["Low"], data["Close"]
        )
        if check is not None and check.tail(1).item() != 0:
            dict["Pattern"] = (self.findCurrentSavedValue(dict,saveDict,"Pattern")[0] + 
                colorText.GREEN + f"Morning Star" + colorText.END 
            )
            saveDict["Pattern"] = self.findCurrentSavedValue(dict,saveDict,"Pattern")[1] +  f"Morning Star"
            hasCandleStickPattern = True

        check = pktalib.CDLMORNINGDOJISTAR(
            data["Open"], data["High"], data["Low"], data["Close"]
        )
        if check is not None and check.tail(1).item() != 0:
            dict["Pattern"] = (self.findCurrentSavedValue(dict,saveDict,"Pattern")[0] + 
                colorText.GREEN + f"Morning Doji Star" + colorText.END 
            )
            saveDict["Pattern"] = self.findCurrentSavedValue(dict,saveDict,"Pattern")[1] +  f"Morning Doji Star"
            hasCandleStickPattern = True

        check = pktalib.CDLEVENINGSTAR(
            data["Open"], data["High"], data["Low"], data["Close"]
        )
        if check is not None and check.tail(1).item() != 0:
            dict["Pattern"] = (self.findCurrentSavedValue(dict,saveDict,"Pattern")[0] + 
                colorText.FAIL + f"Evening Star" + colorText.END 
            )
            saveDict["Pattern"] = self.findCurrentSavedValue(dict,saveDict,"Pattern")[1] +  f"Evening Star"
            hasCandleStickPattern = True

        check = pktalib.CDLEVENINGDOJISTAR(
            data["Open"], data["High"], data["Low"], data["Close"]
        )
        if check is not None and check.tail(1).item() != 0:
            dict["Pattern"] = (self.findCurrentSavedValue(dict,saveDict,"Pattern")[0] + 
                colorText.FAIL + f"Evening Doji Star" + colorText.END 
            )
            saveDict["Pattern"] = self.findCurrentSavedValue(dict,saveDict,"Pattern")[1] +  f"Evening Doji Star"
            hasCandleStickPattern = True

        check = pktalib.CDLLADDERBOTTOM(
            data["Open"], data["High"], data["Low"], data["Close"]
        )
        if check is not None and check.tail(1).item() != 0:
            if check.tail(1).item() > 0:
                dict["Pattern"] = (self.findCurrentSavedValue(dict,saveDict,"Pattern")[0] + 
                    colorText.GREEN + f"Bullish Ladder Bottom" + colorText.END 
                )
                saveDict["Pattern"] = self.findCurrentSavedValue(dict,saveDict,"Pattern")[1] +  f"Bullish Ladder Bottom"
            else:
                dict["Pattern"] = (self.findCurrentSavedValue(dict,saveDict,"Pattern")[0] + 
                    colorText.FAIL + f"Bearish Ladder Bottom" + colorText.END 
                )
                saveDict["Pattern"] = self.findCurrentSavedValue(dict,saveDict,"Pattern")[1] +  f"Bearish Ladder Bottom"
            hasCandleStickPattern = True

        check = pktalib.CDL3LINESTRIKE(
            data["Open"], data["High"], data["Low"], data["Close"]
        )
        if check is not None and check.tail(1).item() != 0:
            if check.tail(1).item() > 0:
                dict["Pattern"] = (self.findCurrentSavedValue(dict,saveDict,"Pattern")[0] + 
                    colorText.GREEN + f"3 Line Strike" + colorText.END 
                )
            else:
                dict["Pattern"] = (self.findCurrentSavedValue(dict,saveDict,"Pattern")[0] + 
                    colorText.FAIL + f"3 Line Strike" + colorText.END 
                )
            saveDict["Pattern"] = self.findCurrentSavedValue(dict,saveDict,"Pattern")[1] +  f"3 Line Strike"
            hasCandleStickPattern = True

        check = pktalib.CDL3BLACKCROWS(
            data["Open"], data["High"], data["Low"], data["Close"]
        )
        if check is not None and check.tail(1).item() != 0:
            dict["Pattern"] = (self.findCurrentSavedValue(dict,saveDict,"Pattern")[0] + 
                colorText.FAIL + f"3 Black Crows" + colorText.END 
            )
            saveDict["Pattern"] = self.findCurrentSavedValue(dict,saveDict,"Pattern")[1] +  f"3 Black Crows"
            hasCandleStickPattern = True

        check = pktalib.CDL3INSIDE(
            data["Open"], data["High"], data["Low"], data["Close"]
        )
        if check is not None and check.tail(1).item() != 0:
            if check.tail(1).item() > 0:
                dict["Pattern"] = (self.findCurrentSavedValue(dict,saveDict,"Pattern")[0] + 
                    colorText.GREEN + f"3 Inside Up" + colorText.END 
                )
                saveDict["Pattern"] = self.findCurrentSavedValue(dict,saveDict,"Pattern")[1] +  f"3 Outside Up"
            else:
                dict["Pattern"] = (self.findCurrentSavedValue(dict,saveDict,"Pattern")[0] + 
                    colorText.FAIL + f"3 Inside Down" + colorText.END 
                )
                saveDict["Pattern"] = self.findCurrentSavedValue(dict,saveDict,"Pattern")[1] +  f"3 Inside Down"
            hasCandleStickPattern = True

        check = pktalib.CDL3OUTSIDE(
            data["Open"], data["High"], data["Low"], data["Close"]
        )
        if check is not None and check.tail(1).item() != 0:
            if check.tail(1).item() > 0:
                dict["Pattern"] = (self.findCurrentSavedValue(dict,saveDict,"Pattern")[0] + 
                    colorText.GREEN + f"3 Outside Up" + colorText.END 
                )
                saveDict["Pattern"] = self.findCurrentSavedValue(dict,saveDict,"Pattern")[1] +  f"3 Outside Up"
            else:
                dict["Pattern"] = (self.findCurrentSavedValue(dict,saveDict,"Pattern")[0] + 
                    colorText.FAIL + f"3 Outside Down" + colorText.END 
                )
                saveDict["Pattern"] = self.findCurrentSavedValue(dict,saveDict,"Pattern")[1] +  f"3 Outside Down"
            hasCandleStickPattern = True

        check = pktalib.CDL3WHITESOLDIERS(
            data["Open"], data["High"], data["Low"], data["Close"]
        )
        if check is not None and check.tail(1).item() != 0:
            dict["Pattern"] = (self.findCurrentSavedValue(dict,saveDict,"Pattern")[0] + 
                colorText.GREEN + f"3 White Soldiers" + colorText.END 
            )
            saveDict["Pattern"] = self.findCurrentSavedValue(dict,saveDict,"Pattern")[1] +  f"3 White Soldiers"
            hasCandleStickPattern = True

        check = pktalib.CDLHARAMI(
            data["Open"], data["High"], data["Low"], data["Close"]
        )
        if check is not None and check.tail(1).item() != 0:
            if check.tail(1).item() > 0:
                dict["Pattern"] = (self.findCurrentSavedValue(dict,saveDict,"Pattern")[0] + 
                    colorText.GREEN + f"Bullish Harami" + colorText.END 
                )
                saveDict["Pattern"] = self.findCurrentSavedValue(dict,saveDict,"Pattern")[1] +  f"Bullish Harami"
            else:
                dict["Pattern"] = (self.findCurrentSavedValue(dict,saveDict,"Pattern")[0] + 
                    colorText.FAIL + f"Bearish Harami" + colorText.END 
                )
                saveDict["Pattern"] = self.findCurrentSavedValue(dict,saveDict,"Pattern")[1] +  f"Bearish Harami"
            hasCandleStickPattern = True

        check = pktalib.CDLHARAMICROSS(
            data["Open"], data["High"], data["Low"], data["Close"]
        )
        if check is not None and check.tail(1).item() != 0:
            if check.tail(1).item() > 0:
                dict["Pattern"] = (self.findCurrentSavedValue(dict,saveDict,"Pattern")[0] + 
                    colorText.GREEN
                    + f"Bullish Harami Cross" 
                    + colorText.END
                )
                saveDict["Pattern"] = self.findCurrentSavedValue(dict,saveDict,"Pattern")[1] +  f"Bullish Harami Cross"
            else:
                dict["Pattern"] = (self.findCurrentSavedValue(dict,saveDict,"Pattern")[0] + 
                    colorText.FAIL
                    + f"Bearish Harami Cross" 
                    + colorText.END
                )
                saveDict["Pattern"] = self.findCurrentSavedValue(dict,saveDict,"Pattern")[1] +  f"Bearish Harami Cross"
            hasCandleStickPattern = True

        check = pktalib.CDLMARUBOZU(
            data["Open"], data["High"], data["Low"], data["Close"]
        )
        if check is not None and check.tail(1).item() != 0:
            if check.tail(1).item() > 0:
                dict["Pattern"] = (self.findCurrentSavedValue(dict,saveDict,"Pattern")[0] + 
                    colorText.GREEN
                    + f"Bullish Marubozu" 
                    + colorText.END
                )
                saveDict["Pattern"] = self.findCurrentSavedValue(dict,saveDict,"Pattern")[1] +  f"Bullish Marubozu"
            else:
                dict["Pattern"] = (
                    colorText.FAIL + f"Bearish Marubozu" + colorText.END 
                )
                saveDict["Pattern"] = self.findCurrentSavedValue(dict,saveDict,"Pattern")[1] +  f"Bearish Marubozu"
            hasCandleStickPattern = True

        check = pktalib.CDLHANGINGMAN(
            data["Open"], data["High"], data["Low"], data["Close"]
        )
        if check is not None and check.tail(1).item() != 0:
            dict["Pattern"] = (self.findCurrentSavedValue(dict,saveDict,"Pattern")[0] + 
                colorText.FAIL + f"Hanging Man" + colorText.END 
            )
            saveDict["Pattern"] = self.findCurrentSavedValue(dict,saveDict,"Pattern")[1] +  f"Hanging Man"
            hasCandleStickPattern = True

        check = pktalib.CDLHAMMER(
            data["Open"], data["High"], data["Low"], data["Close"]
        )
        if check is not None and check.tail(1).item() != 0:
            dict["Pattern"] = (self.findCurrentSavedValue(dict,saveDict,"Pattern")[0] + 
                colorText.GREEN + f"Hammer" + colorText.END 
            )
            saveDict["Pattern"] = self.findCurrentSavedValue(dict,saveDict,"Pattern")[1] +  f"Hammer"
            hasCandleStickPattern = True

        check = pktalib.CDLINVERTEDHAMMER(
            data["Open"], data["High"], data["Low"], data["Close"]
        )
        if check is not None and check.tail(1).item() != 0:
            dict["Pattern"] = (self.findCurrentSavedValue(dict,saveDict,"Pattern")[0] + 
                colorText.GREEN + f"Inverted Hammer" + colorText.END 
            )
            saveDict["Pattern"] = self.findCurrentSavedValue(dict,saveDict,"Pattern")[1] +  f"Inverted Hammer"
            hasCandleStickPattern = True

        check = pktalib.CDLSHOOTINGSTAR(
            data["Open"], data["High"], data["Low"], data["Close"]
        )
        if check is not None and check.tail(1).item() != 0:
            dict["Pattern"] = (self.findCurrentSavedValue(dict,saveDict,"Pattern")[0] + 
                colorText.FAIL + f"Shooting Star" + colorText.END 
            )
            saveDict["Pattern"] = self.findCurrentSavedValue(dict,saveDict,"Pattern")[1] +  f"Shooting Star"
            hasCandleStickPattern = True

        check = pktalib.CDLDRAGONFLYDOJI(
            data["Open"], data["High"], data["Low"], data["Close"]
        )
        if check is not None and check.tail(1).item() != 0:
            dict["Pattern"] = (self.findCurrentSavedValue(dict,saveDict,"Pattern")[0] + 
                colorText.GREEN + f"Dragonfly Doji" + colorText.END 
            )
            saveDict["Pattern"] = self.findCurrentSavedValue(dict,saveDict,"Pattern")[1] +  f"Dragonfly Doji"
            hasCandleStickPattern = True

        check = pktalib.CDLGRAVESTONEDOJI(
            data["Open"], data["High"], data["Low"], data["Close"]
        )
        if check is not None and check.tail(1).item() != 0:
            dict["Pattern"] = (self.findCurrentSavedValue(dict,saveDict,"Pattern")[0] + 
                colorText.FAIL + f"Gravestone Doji" + colorText.END 
            )
            saveDict["Pattern"] = self.findCurrentSavedValue(dict,saveDict,"Pattern")[1] +  f"Gravestone Doji"
            hasCandleStickPattern = True

        check = pktalib.CDLENGULFING(
            data["Open"], data["High"], data["Low"], data["Close"]
        )
        if check is not None and check.tail(1).item() != 0:
            if check.tail(1).item() > 0:
                dict["Pattern"] = (self.findCurrentSavedValue(dict,saveDict,"Pattern")[0] + 
                    colorText.GREEN
                    + f"Bullish Engulfing" 
                    + colorText.END
                )
                saveDict["Pattern"] = self.findCurrentSavedValue(dict,saveDict,"Pattern")[1] +  f"Bullish Engulfing"
            else:
                dict["Pattern"] = (self.findCurrentSavedValue(dict,saveDict,"Pattern")[0] + 
                    colorText.FAIL
                    + f"Bearish Engulfing" 
                    + colorText.END
                )
                saveDict["Pattern"] = self.findCurrentSavedValue(dict,saveDict,"Pattern")[1] +  f"Bearish Engulfing"
            hasCandleStickPattern = True
        if hasCandleStickPattern:
            return True
        return False
