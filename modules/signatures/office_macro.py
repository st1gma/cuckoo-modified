# Copyright (C) 2012-2015 KillerInstinct
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from lib.cuckoo.common.abstracts import Signature

class Office_Macro(Signature):
    name = "office_macro"
    description = "The office file has a macro."
    severity = 2
    categories = ["office"]
    authors = ["KillerInstinct"]
    minimum = "0.5"

    def run(self):
        ret = False
        if "static" in self.results:
            if "Macro" in self.results["static"]:
                if "Code" in self.results["static"]["Macro"]:
                    ret = True
                    total = len(self.results["static"]["Macro"]["Code"])
                    if total > 1:
                        self.description = "The office file has %s macros." % str(total)

        if ret and "strings" in self.results:
            lures = ["bank account",
                     "enable content",
                     "tools > macro",
                     "macros must be enabled",
                    ]
            positives = list()
            for string in self.results["strings"]:
                for lure in lures:
                    if lure in string.lower():
                        if string not in positives:
                            positives.append(string)

            if positives != []:
                self.severity = 3
                self.description += " The file also appears to have strings indicating common phishing lures."
                for positive in positives:
                    self.data.append({"Lure": positive})

        return ret
