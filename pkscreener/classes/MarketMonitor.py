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
import sys
import pandas as pd
import numpy as np
from PKDevTools.classes.Singleton import SingletonType, SingletonMixin
from PKDevTools.classes.OutputControls import OutputControls
from PKDevTools.classes.ColorText import colorText
from pkscreener.classes import Utility

class MarketMonitor(SingletonMixin, metaclass=SingletonType):
    def __init__(self,monitors=[]):
        super(MarketMonitor, self).__init__()
        if monitors is not None and len(monitors) > 0:
            self.monitors = monitors
            self.monitorIndex = 0
            self.monitorPositions = {}
            # We are going to present the dataframes in a 3x3 matrix with limited set of columns
            rowIndex = 0
            colIndex = 0
            self.maxNumRowsInEachResult = 10
            self.maxNumColsInEachResult = 6
            self.maxNumResultsPerRow = 5
            maxColIndex = self.maxNumColsInEachResult * self.maxNumResultsPerRow - 1
            self.lines = 0
            for monitorKey in monitors:
                self.monitorPositions[monitorKey] = [rowIndex,colIndex]
                colIndex += self.maxNumColsInEachResult
                if colIndex > maxColIndex:
                    colIndex = 0
                    rowIndex += self.maxNumRowsInEachResult
            columns = []
            colNameIndex = 0
            maxColIndex = min(maxColIndex,len(self.monitorPositions)*self.maxNumColsInEachResult -1)
            while colNameIndex <= maxColIndex:
                columns.append(f"A{colNameIndex +1}")
                colNameIndex += 1
            self.monitor_df = pd.DataFrame(columns=columns)

    def currentMonitorOption(self):
        try:
            option = None
            maxIndex = len(self.monitors) -1
            option = str(self.monitors[self.monitorIndex:self.monitorIndex+1][0])
            self.monitorIndex += 1
            if self.monitorIndex > maxIndex:
                self.monitorIndex = 0
        except:
            pass
        return option

    def refresh(self, screen_df:pd.DataFrame=None, screenOptions=None, chosenMenu=None):
        highlightRows = []
        highlightCols = []
        if screen_df is None or screen_df.empty:
            return

        screen_monitor_df = screen_df.copy()
        screen_monitor_df.reset_index(inplace=True)
        screen_monitor_df = screen_monitor_df[["Stock", "LTP", "%Chng","52Wk H","RSI","Volume"]].head(self.maxNumRowsInEachResult-1)
        screen_monitor_df.loc[:, "%Chng"] = screen_monitor_df.loc[:, "%Chng"].apply(
                    lambda x: Utility.tools.roundOff(str(x).split("% (")[0] + colorText.END,0)
                )
        screen_monitor_df.loc[:, "52Wk H"] = screen_monitor_df.loc[:, "52Wk H"].apply(
            lambda x: Utility.tools.roundOff(x,0)
        )
        screen_monitor_df.loc[:, "Volume"] = screen_monitor_df.loc[:, "Volume"].apply(
            lambda x: Utility.tools.roundOff(x,0)
        )
        screen_monitor_df.rename(columns={"%Chng": "Ch%","Volume":"Vol","52Wk H":"52WkH"}, inplace=True)
        monitorPosition = self.monitorPositions.get(screenOptions)
        if monitorPosition is not None:
            startRowIndex, startColIndex = monitorPosition
            if not self.monitor_df.empty:
                for _ in range(self.lines):
                    sys.stdout.write("\x1b[1A")  # cursor up one line
                    sys.stdout.write("\x1b[2K")  # delete the last line

            firstColIndex = startColIndex
            rowIndex = 0
            colIndex = 0
            highlightRows = [startRowIndex]
            highlightCols = []
            while rowIndex <= len(screen_monitor_df):
                for col in screen_monitor_df.columns:
                    if rowIndex == 0:
                        # Column names to be repeated for each refresh in respective headers
                        widgetHeader = ":".join(screenOptions.replace(":D","").split(":")[:4])
                        self.monitor_df.loc[startRowIndex,[f"A{startColIndex+1}"]] = colorText.BOLD+colorText.HEAD+(widgetHeader if startColIndex==firstColIndex else col)+colorText.END
                        highlightCols.append(startColIndex)
                    else:
                        self.monitor_df.loc[startRowIndex, [f"A{startColIndex+1}"]] = screen_monitor_df.iloc[rowIndex-1,colIndex]
                        colIndex += 1
                    startColIndex += 1
                _, startColIndex= monitorPosition
                rowIndex += 1
                colIndex = 0
                highlightRows.append(startRowIndex+1)
                startRowIndex += 1

        self.monitor_df = self.monitor_df.replace(np.nan, "-", regex=True)
        OutputControls().printOutput(
            colorText.BOLD
            + colorText.FAIL
            + "[+] You chose: (Dashboard) > "
            + f"{chosenMenu} [{screenOptions}]"
            + colorText.END
            , enableMultipleLineOutput=True
        )
        tabulated_results = colorText.miniTabulator().tabulate(
            self.monitor_df, tablefmt=colorText.No_Pad_GridFormat,
            highlightCharacter=colorText.HEAD+"="+colorText.END,
            showindex=False,
            highlightedRows=highlightRows,
            highlightedColumns=highlightCols,
            maxcolwidths=Utility.tools.getMaxColumnWidths(self.monitor_df)
        )
        self.lines = len(tabulated_results.splitlines()) + 1 # 1 for the progress bar at the bottom and 1 for the chosenMenu option
        OutputControls().printOutput(tabulated_results, enableMultipleLineOutput=True)
