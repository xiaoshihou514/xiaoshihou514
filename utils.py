def fmt_lines(n):
    """Format LOC as 1k, 1.2k, etc."""
    return f"{n / 1000:.1f}k" if n >= 1000 else str(n)


def trunc(s, n=12):
    """Truncate name to max n chars."""
    return s if len(s) <= n else s[: n - 1] + "…"


def generate_svg(lang_stats, output_file, total_lines, title=None):
    """
    Generate SVG chart from language statistics
    
    Args:
        lang_stats: List of dictionaries with keys: name, lines, percent, color
        output_file: Path to output SVG file
        total_lines: Total lines of code
        title: Optional title for the chart
    """
    # SVG setup
    width = 800
    bar_height = 50
    gap = 30
    stats_gap = 30
    circle_radius = 6
    text_line_height = 20
    height = bar_height + gap + ((len(lang_stats) + 2) // 3) * text_line_height + 50

    # Start SVG
    svg_lines = [
        f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">',
        f'<rect width="{width}" height="{height}" fill="#212830"/>',
    ]

    # Add title if provided
    if title:
        svg_lines.append(
            f'<text x="10" y="30" font-size="18" font-family="sans-serif" fill="#FFF" font-weight="bold">{title}</text>'
        )

    # Draw horizontal stacked bar
    x = 10
    y = 40 if not title else 60
    for lang in lang_stats:
        bar_width = width * lang["percent"] / 100
        svg_lines.append(
            f'<rect x="{x}" y="{y}" width="{bar_width}" height="{bar_height}" fill="{lang["color"]}"/>'
        )
        x += bar_width  # move to next segment

    # Draw language stats below (3 per line) with colored circle
    y_stats = y + bar_height + stats_gap
    count = 0
    x_text = 10
    for lang in lang_stats:
        # Circle
        svg_lines.append(
            f'<circle cx="{x_text + circle_radius}" cy="{y_stats - 4}" r="{circle_radius}" fill="{lang["color"]}" />'
        )
        # Text
        name = trunc(lang["name"])
        lines_str = fmt_lines(lang["lines"])

        text = f"{name} ({lines_str} lines, {lang['percent']:.1f}%)"
        svg_lines.append(
            f'<text x="{x_text + 2 * circle_radius + 5}" y="{y_stats}" font-size="15" font-family="sans-serif" fill="#FFF">{text}</text>'
        )
        count += 1
        if count % 3 == 0:
            y_stats += text_line_height  # next line
            x_text = 10
        else:
            x_text += 250  # adjust spacing between columns

    svg_lines.append("</svg>")

    # Write SVG
    with open(output_file, "w") as f:
        f.write("\n".join(svg_lines))

    print(f"Total lines: {total_lines}")
    print(f"SVG generated: {output_file}")
