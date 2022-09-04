import uiautomation as api32
import pyautogui as auto

from JianYingApi.Logic_warp import lag
from . import Ui_warp
from threading import Thread

Half = Ui_warp._search_include(windowObj=api32.WindowControl(searchDepth=1,Name="JianyingPro"),controlType=api32.PaneControl,ClassName="SplitView")
Pin = Half.GroupControl(searchDepth=1,Name="MainTimeLineRoot").GroupControl(searchDepth=1,Name="TimeLineRulerAdsorb")
def _current_progress()->api32.TextControl:
    return Half.TextControl(Name="currentProgress",searchDepth=1).GroupControl().Name
def _total_progress()->api32.TextControl:
    return Half.TextControl(Name="totalProgress",searchDepth=1).GroupControl().Name

def _to_mil_sec(a:str)->int:
    _t = a.split(":")
    return int(_t[0])*3600 + int(_t[1])*60 + int(_t[2])
        

class Bind_Element:
    def __init__(self,Element:api32.GroupControl) -> None:
        self.ele = Element
        auto.click(Element.BoundingRectangle.left,Pin.BoundingRectangle.ycenter())
        self.Start = _to_mil_sec(_current_progress())
        auto.click(Element.BoundingRectangle.right,Pin.BoundingRectangle.ycenter())
        self.End = _to_mil_sec(_current_progress())
        self.Duration = self.End - self.Start
        print(self.Start,self.End,self.Duration)

    def Cut(self,Start:int,End:int):
        assert Start < self.Duration , IndexError
        assert End < self.Duration , IndexError

    def Expand(self,Start:int,End:int,tolerance:int=0,Step:int=10):
        """
            Expand Elements
        """
        auto.click(self.ele.BoundingRectangle.left,Pin.BoundingRectangle.ycenter())
        if abs( self.Start - Start ) > tolerance :
            api32.PressMouse(x=self.ele.BoundingRectangle.left,y=self.ele.BoundingRectangle.ycenter())
            while abs( _to_mil_sec(_current_progress()) - Start ) > tolerance:
                if _to_mil_sec(_current_progress()) > Start: api32.MoveTo(x=self.ele.BoundingRectangle.left-Step,y=self.ele.BoundingRectangle.ycenter())
                if _to_mil_sec(_current_progress()) < Start: api32.MoveTo(x=self.ele.BoundingRectangle.left+Step,y=self.ele.BoundingRectangle.ycenter())
                break
            api32.ReleaseMouse()

        if abs( self.End - End ) > tolerance :
            api32.PressMouse(x=self.ele.BoundingRectangle.right,y=self.ele.BoundingRectangle.ycenter())
            while abs( _to_mil_sec(_current_progress()) - End ) > tolerance:
                if _to_mil_sec(_current_progress()) > End: api32.MoveTo(x=self.ele.BoundingRectangle.right-Step,y=self.ele.BoundingRectangle.ycenter())
                if _to_mil_sec(_current_progress()) < End: api32.MoveTo(x=self.ele.BoundingRectangle.right+Step,y=self.ele.BoundingRectangle.ycenter())
                break
            api32.ReleaseMouse()