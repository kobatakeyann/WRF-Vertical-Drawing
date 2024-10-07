from constant import LAT_END, LAT_START, LON_END, LON_START, TITLE
from time_relation.conversion import PaddingDatetime


class TextAquisition(PaddingDatetime):
    def get_title_text(self) -> str:
        if LAT_START == LAT_END:
            section_location = f"{LON_START}-{LON_END}°E at {LAT_START}°N"
        elif LON_START == LON_END:
            section_location = f"{LAT_START}-{LAT_END}°N at {LON_START}°E"
        else:
            section_location = (
                f"{LAT_START}-{LAT_END}°N, {LON_START}-{LON_END}°E"
            )
        title = f"{self.year}/{self.month}/{self.day} {self.hour}{self.minute}JST   {section_location}  {TITLE}"
        return title

    def get_filename(self) -> str:
        filename = f"{self.year}{self.month}{self.day}_{self.hour}{self.minute}JST.jpg"
        return filename
