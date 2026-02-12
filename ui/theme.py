
class Theme:
    # Colors
    COLOR_BG = "#0F172A"       # Main Window Background (Slate-900)
    COLOR_SURFACE = "#1E293B"  # Sidebar, Cards (Slate-800)
    COLOR_PRIMARY = "#F97316"  # Action Buttons (Orange-500)
    COLOR_PRIMARY_HOVER = "#EA580C" # Orange-600
    
    COLOR_SECONDARY = "#334155" # Input, Secondary Buttons (Slate-700)
    COLOR_SECONDARY_HOVER = "#475569" # Slate-600
    
    COLOR_TEXT_PRIMARY = "#F1F5F9"   # Slate-100
    COLOR_TEXT_SECONDARY = "#94A3B8" # Slate-400
    
    COLOR_BORDER = "#475569"   # Slate-600
    
    COLOR_SUCCESS = "#22C55E"  # Green-500
    COLOR_ERROR = "#EF4444"    # Red-500
    
    # Fonts
    FONT_FAMILY = "Inter"      # Fallback to system if not found
    
    # Dimensions
    CORNER_RADIUS = 0          # Industrial look
    BORDER_WIDTH = 1
    
    @classmethod
    def apply_entry_style(cls, entry):
        entry.configure(
            fg_color=cls.COLOR_SECONDARY,
            border_color=cls.COLOR_BORDER,
            text_color=cls.COLOR_TEXT_PRIMARY,
            placeholder_text_color=cls.COLOR_TEXT_SECONDARY,
            corner_radius=cls.CORNER_RADIUS
        )

    @classmethod
    def apply_button_primary(cls, button):
        button.configure(
            fg_color=cls.COLOR_PRIMARY,
            hover_color=cls.COLOR_PRIMARY_HOVER,
            text_color=cls.COLOR_TEXT_PRIMARY,
            corner_radius=cls.CORNER_RADIUS
        )
        
    @classmethod
    def apply_button_secondary(cls, button):
        button.configure(
            fg_color=cls.COLOR_SECONDARY,
            hover_color=cls.COLOR_SECONDARY_HOVER,
            text_color=cls.COLOR_TEXT_PRIMARY,
            corner_radius=cls.CORNER_RADIUS,
            border_width=cls.BORDER_WIDTH,
            border_color=cls.COLOR_BORDER
        )
