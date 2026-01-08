"""
Demo Data Module
Contains demo greeting configurations and seasonal presets for the Interactive Demo tab
"""

from typing import Dict, List
from dataclasses import dataclass
from datetime import datetime


@dataclass
class DemoGreeting:
    """Represents a demo greeting configuration"""
    from_name: str
    to_name: str
    occasion: str
    message: str
    theme: str
    animation: str
    created_at: str = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().isoformat() + "Z"
    
    def to_dict(self) -> Dict:
        return {
            "from": self.from_name,
            "to": self.to_name,
            "occasion": self.occasion,
            "message": self.message,
            "theme": self.theme,
            "animation": self.animation,
            "created": self.created_at
        }


# Seasonal demo greetings (rotate based on date)
SEASONAL_DEMOS: Dict[str, DemoGreeting] = {
    "christmas": DemoGreeting(
        from_name="Sarah",
        to_name="Mike",
        occasion="Christmas 2025",
        message="Wishing you a magical holiday season filled with joy, laughter, and special moments with loved ones!",
        theme="snowflake",
        animation="FadeInCenterOut"
    ),
    "newyear": DemoGreeting(
        from_name="Alex",
        to_name="Jordan",
        occasion="New Year 2026",
        message="Here's to new beginnings, fresh starts, and amazing adventures in the year ahead!",
        theme="fireworks",
        animation="RadialRipple"
    ),
    "valentine": DemoGreeting(
        from_name="Emma",
        to_name="James",
        occasion="Valentine's Day",
        message="To the person who makes every day feel like a celebration. Happy Valentine's Day!",
        theme="hearts",
        animation="FadeInCenterOut"
    ),
    "wedding": DemoGreeting(
        from_name="Friends",
        to_name="The Happy Couple",
        occasion="Wedding Day",
        message="Congratulations on your special day! Wishing you a lifetime of love and happiness together.",
        theme="champagne",
        animation="RadialRipple"
    ),
    "general": DemoGreeting(
        from_name="You",
        to_name="Someone Special",
        occasion="Any Occasion",
        message="Life is what you make it. Make every moment special and share it with those you love.",
        theme="lights",
        animation="FadeInTopDown"
    )
}


def get_seasonal_demo() -> DemoGreeting:
    """
    Returns appropriate demo based on current date/season
    Falls back to general if not in special season
    """
    month = datetime.now().month
    
    if month == 12:
        return SEASONAL_DEMOS["christmas"]
    elif month == 1:
        return SEASONAL_DEMOS["newyear"]
    elif month == 2:
        return SEASONAL_DEMOS["valentine"]
    else:
        return SEASONAL_DEMOS["general"]


# Occasion presets for quick selection
OCCASION_PRESETS: List[str] = [
    "Birthday",
    "Anniversary",
    "Christmas",
    "New Year",
    "Wedding",
    "Graduation",
    "Congratulations",
    "Thank You",
    "Get Well",
    "Just Because"
]


# Animation presets per theme
ANIMATION_PRESETS: Dict[str, List[str]] = {
    "snowflake": ["FadeInCenterOut", "FadeInTopDown"],
    "fireworks": ["RadialRipple", "MaterializeIn"],
    "lights": ["FadeInTopDown", "FadeInCenterOut"],
    "stars": ["RadialRippleIn", "MaterializeIn"],
    "confetti": ["MaterializeIn", "RadialRipple"],
    "champagne": ["RadialRipple", "FadeInCenterOut"],
    "hearts": ["FadeInCenterOut", "FadeInTopDown"],
    "valentine": ["FadeInCenterOut", "RadialRipple"],
    "farewell": ["FadeInTopDown", "FadeInCenterOut"],
}
