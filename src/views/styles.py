class UIStyles:
    """
    View Layer Styles: Design tokens for the custom dark-theme GUI layout.
    Specifies color vectors [R, G, B, A] for drawing shapes and text.
    """
    # Slate Charcoal background (90% contrast)
    BG_COLOR = [0.07, 0.07, 0.08, 1.0]
    BG_HEX = "#121214"
    
    # Deep Steel card elements
    CARD_COLOR = [0.12, 0.12, 0.14, 1.0]
    CARD_HEX = "#1E1E24"
    
    # Primary Accent: Electric Violet
    ACCENT_COLOR = [0.49, 0.30, 1.00, 1.0]
    ACCENT_HEX = "#7C4DFF"
    
    # Priority indicators
    HIGH_PRIORITY = [1.00, 0.34, 0.13, 1.0]   # Neon Tangerine
    MED_PRIORITY = [1.00, 0.70, 0.00, 1.0]    # Warm Amber
    LOW_PRIORITY = [0.00, 0.90, 1.00, 1.0]    # Vibrant Cyan
    
    # Text colors
    TEXT_PRIMARY = [1.00, 1.00, 1.00, 1.0]    # White
    TEXT_SECONDARY = [0.56, 0.56, 0.62, 1.0]  # Soft Grey
    TEXT_MUTED = [0.35, 0.35, 0.40, 1.0]      # Dark Muted Grey
    
    # Alert states
    ERROR_RED = [1.00, 0.20, 0.20, 1.0]       # Vibrant Red
    SUCCESS_GREEN = [0.10, 0.80, 0.40, 1.0]   # Clear Mint Green
    
    # Layout and padding constants
    PADDING_OUTER = 16
    PADDING_INNER = 12
    SPACING_GUTTER = 10
    RADIUS_CARD = [12]
    RADIUS_BUTTON = [8]

    @staticmethod
    def get_priority_color(priority: str) -> list[float]:
        """Maps a priority level string to its corresponding UI color vector."""
        p_lower = priority.lower().strip()
        if p_lower == "high":
            return UIStyles.HIGH_PRIORITY
        elif p_lower == "medium":
            return UIStyles.MED_PRIORITY
        return UIStyles.LOW_PRIORITY
