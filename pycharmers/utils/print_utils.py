# coding: utf-8
import re
from ._colorings import _toCOLOR_create
from .generic_utils import handleKeyError, handleTypeError

f_aligns           = ["<", ">", "=", "^"]
f_signs            = ["+", "-", " ", ""]
f_grouping_options = ["_", ",", ""]
f_types            = ["b", "c", "d", "e", "E", "f", "F", "g", "G", "n", "o", "s", "x", "X", "%"]

def format_spec_create(align=">", sign="", zero_padding=False, width=0, grouping_option="", fmt=""):
    """Create a function which returns a formatted text.

    `format_spec = [[fill]align][sign][#][0][width][grouping_option][.precision][type]`

    Args:
        width
        align (str)           : [[fill]align] One of ``["<", ">", "=", "^"]``
        sign (str)            : [sign] One of ``["+", "-", " ", ""]``
        zero_padding (bool)   : [0]
        width (int)           : [width]
        grouping_option (str) : [grouping_option] One of ``["_", ",", ""]``
        fmt (str)             : [.precision][type] One of ``["b", "c", "d", "e", "E", "f", "F", "g", "G", "n", "o", "s", "x", "X", "%"]``

    Returns:
        format_spec: lambda (`<function __main__.<lambda>(fill)>`)
        
    References:
        - `Python Source Code <https://github.com/python/cpython/blob/3.8/Lib/string.py>`_ 
        - `Python Documentation <https://docs.python.org/3/library/string.html#format-specification-mini-language>`_

    Examples:
        >>> from pycharmers.utils import format_spec_create
        >>> format_spec = format_spec_create(width=10, align="^")
        >>> format_spec("hoge")
        '   hoge   '
        >>> format_spec = format_spec_create(align="<", fmt=".1%")
        >>> format_spec(1/3)
        '33.3%'
        >>> format_spec = format_spec_create(align=">", zero_padding=True, fmt="b")
        >>> format_spec(20)
        '10100'
    """
    handleKeyError(lst=f_aligns, align=align)
    handleKeyError(lst=f_signs,  sign=sign)
    handleKeyError(lst=f_grouping_options, grouping_option=grouping_option)
    if len(fmt)>0:
        handleKeyError(lst=f_types, fmt=fmt[-1])
    zero = "0" if zero_padding else ""
    handleTypeError(types=[int], width=width)
    return lambda fill : f"{fill:{align}{sign}{zero}{width}{grouping_option}{fmt}}"

def print_func_create(align=">", sign="", zero_padding=False, width=0, 
                      grouping_option="", fmt="", color="black",
                      left_side_bar="", right_side_bar="",
                      left_margin=0, right_margin=0, end="\n"):
    """Create a function which prints a formatted text. Please see also the function `format_spec_create`.
    
    Args:
        color (str)                : color
        left(right)_side_bar (str) : Characters to output to the Left/Right side.
        left(right)_margin (int)   : Left/Right side margin
        end (str)                  : string appended after the last value, default a newline.
    
    Returns:
        print_func: Function that can be used like print

    Examples:
        >>> from pycharmers.utils import print_func_create
        >>> print_func = print_func_create(width=8, align="^", left_side_bar="[", right_side_bar="]")
        >>> print_func("hoge")
        [  hoge  ]
        >>> print_func = print_func_create(align="<", left_side_bar="$ ")
        >>> print_func("git clone https://github.com/iwasakishuto/Python-utils.git")
        $ git clone https://github.com/iwasakishuto/Python-utils.git
        >>> print_func("cd Python-utils")
        $ cd Python-utils
        >>> print_func("sudo python setup.py install")
        $ sudo python setup.py install
    """
    format_spec = format_spec_create(
        align=align, sign=sign, zero_padding=zero_padding,
        width=width, grouping_option=grouping_option, fmt=fmt
    )
    toCOLOR = _toCOLOR_create(color)
    def print_func(fill):
        info  = f"{left_side_bar}{' '*left_margin}"
        info += toCOLOR(format_spec(fill))
        info += f"{' '*right_margin}{right_side_bar}"
        print(info, end=end)
    return print_func

class Table():
    """Create a beautiful table and show.

    Properties:
        ncols(int) : the number of columns.

    Methods:
        set_cols : Set values to a table.
        show     : Show a table.

    Examples:
        >>> from pycharmers.utils import Table
        >>> table = Table()
        >>> table.set_cols(range(3), colname="id")
        >>> table.set_cols(list("abc"))
        >>> table.show()
        |id|col.2|
        ==========
        | 0|    a|
        | 1|    b|
        | 2|    c|
    """
    def __init__(self):
        self.cols = {}
        self.table_width = 1
        self.head = -1
    
    @property
    def ncols(self):
        return len(self.cols)

    def _disp_title(self):
        for colname, options in self.cols.items():
            if "print_values" not in options:
                continue
            print_func = options.get("print_title")
            print_func(colname)
        print("|")

    def _disp_border(self, table_width=None, mark="="):
        table_width = self.table_width if table_width is None else table_width
        print(mark*table_width)

    def _disp_values(self, head=None):
        head = head or self.head
        for i in range(head):
            for colname, options in self.cols.items():
                if "print_values" not in options:
                    continue
                print_func = options.get("print_values")
                val = options.get("values")[i]
                print_func(val)
            print("|")

    def show(self, head=None, table_width=None, mark="="):
        """Show a table
        
        Args:
            head (str)        : Show the first ``head`` rows for the table. 
            table_width (int) : The table width.
            mark (str)        : border mark. (default "=")
        """
        self._disp_title()
        self._disp_border(table_width=table_width, mark=mark)
        self._disp_values(head=head)

    def set_cols(self, values, colname=None, width=None, align=">", sign="",
                 zero_padding=False, grouping_option="", fmt="", color="black",
                 left_margin=0, right_margin=0):
        """Set values to a table.
        
        Args:
            values (array) : The array-like data.
            colname (str)  : The colname for ``values``.
            **kwargs       : See also ``print_func_create``
        """
        colname = colname or f"col.{self.ncols+1}"
        title_width = len(str(colname))
        if width is None:
            format_spec = format_spec_create(
                width=0, align=align, sign=sign, zero_padding=zero_padding,
                grouping_option=grouping_option, fmt=fmt
            )
            width = len(max([format_spec(v) for v in values], key=len))
        width = max(width, title_width)
        self.table_width += width + left_margin + right_margin + 1

        print_values = print_func_create(
            align=align, sign=sign, zero_padding=zero_padding, width=width,
            grouping_option=grouping_option, fmt=fmt, color=color,
            left_side_bar="|", right_side_bar="", end="",
            left_margin=left_margin, right_margin=right_margin,
        )
        print_title = print_func_create(
            align="^", sign="", zero_padding=False, width=width, 
            grouping_option="", fmt="", color="ACCENT",
            left_side_bar="|", right_side_bar="", end="",
            left_margin=left_margin, right_margin=right_margin,
        )
        self.cols.update({
            colname: {
                "print_values" : print_values,
                "print_title"  : print_title,
                "values"       : values,
            }
        })
        nrows = len(values)
        if self.head==-1 or nrows < self.head:
            self.head = nrows

def print_dict_tree(dictionary, indent=4, rank=0, marks=["-", "*", "#"]):
    """Print Dictionary as a Tree.

    Args:
        dictionary (dict) : An input dictionary.
        indent (int)      : Indent.
        rank (int)        : A current rank.
        marks (list)      : List mark types.

    Examples:
        >>> from pycharmers.utils import print_dict_tree
        >>> print_dict_tree({"a": 0, "b": 1})
        - a: 0
        - b: 1
        >>> print_dict_tree({"a": 0, "b": {"b1": 1, "b2": 2}})
        - a: 0
        - b: 
          * b1: 1
          * b2: 2
        >>> print_dict_tree({"a": 0, "b": {"b1": 1, "b2": {"b21": 0, "b22": 1}}, "c": 3})
        - a: 0
        - b: 
          * b1: 1
          * b2: 
            # b21: 0
            # b22: 1
        - c: 3
    """
    if hasattr(dictionary, "items"):
        for k,v in dictionary.items():
            if hasattr(v, "items"):
                print(f"{' '*indent*rank}{marks[rank%len(marks)]} {k}: ")
                print_dict_tree(dictionary=v, indent=indent, rank=rank+1, marks=marks)
            else:
                print(f"{' '*indent*rank}{marks[rank%len(marks)]} {k}: {v}")

def pretty_3quote(*value, indent=0):
    """pretty 3 quote string.
    
    Args:
        indent (int)  : If indent is a non-negative integer, then multiple lines will be pretty-printed with that indent level.
        
    Examples:
        >>> from pycharmers.utils import pretty_3quote
        >>> print(*pretty_3quote(\"\"\"
            When I was 17, I read a quote that went something like: 
            “If you live each day as if it was your last, someday you’ll most certainly be right.”
            It made an impression on me, and since then, for the past 33 years, 
        \"\"\"))
        When I was 17, I read a quote that went something like: 
        “If you live each day as if it was your last, someday you’ll most certainly be right.”
        It made an impression on me, and since then, for the past 33 years, 
    """
    return [re.sub(pattern=r"\n\s+", repl=r"\n"+r" "*indent, string=val).strip("\n") for val in value]
