"""
Chart Generator Module
Creates beautiful charts from data analysis results using matplotlib.
"""

import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import pandas as pd
import io
import base64
import os


# Style configuration
COLORS = ['#6366f1', '#8b5cf6', '#06b6d4', '#10b981', '#f59e0b', '#ef4444', '#ec4899', '#14b8a6']
BG_COLOR = '#0f172a'
TEXT_COLOR = '#e2e8f0'
GRID_COLOR = '#1e293b'


def setup_style():
    """Apply dark theme styling to matplotlib."""
    plt.rcParams.update({
        'figure.facecolor': BG_COLOR,
        'axes.facecolor': '#1e293b',
        'axes.edgecolor': '#334155',
        'axes.labelcolor': TEXT_COLOR,
        'text.color': TEXT_COLOR,
        'xtick.color': TEXT_COLOR,
        'ytick.color': TEXT_COLOR,
        'grid.color': GRID_COLOR,
        'grid.alpha': 0.3,
        'font.family': 'sans-serif',
        'font.size': 11,
    })


def fig_to_base64(fig) -> str:
    """Convert a matplotlib figure to a base64 string."""
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=150, bbox_inches='tight',
                facecolor=fig.get_facecolor(), edgecolor='none')
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()
    plt.close(fig)
    return img_base64


def save_chart(fig, filename: str, output_dir: str = "static") -> str:
    """Save chart to file and return the path."""
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, filename)
    fig.savefig(filepath, format='png', dpi=150, bbox_inches='tight',
                facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close(fig)
    return filepath


def create_bar_chart(data: dict, title: str, xlabel: str = "", ylabel: str = "") -> str:
    """Create a styled bar chart. Returns base64 image string."""
    setup_style()
    fig, ax = plt.subplots(figsize=(10, 6))

    labels = list(data.keys())
    values = list(data.values())
    bars = ax.bar(labels, values, color=COLORS[:len(labels)], width=0.6,
                  edgecolor='none', alpha=0.9)

    # Add value labels on bars
    for bar, val in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width() / 2., bar.get_height() + max(values) * 0.02,
                f'{val:,.0f}' if isinstance(val, (int, float)) else str(val),
                ha='center', va='bottom', fontsize=10, fontweight='bold', color=TEXT_COLOR)

    ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel(xlabel, fontsize=12, labelpad=10)
    ax.set_ylabel(ylabel, fontsize=12, labelpad=10)
    ax.grid(axis='y', alpha=0.2)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    return fig_to_base64(fig)


def create_line_chart(data: dict, title: str, xlabel: str = "", ylabel: str = "") -> str:
    """Create a styled line chart. Returns base64 image string."""
    setup_style()
    fig, ax = plt.subplots(figsize=(10, 6))

    labels = list(data.keys())
    values = list(data.values())

    ax.plot(labels, values, color=COLORS[0], linewidth=2.5, marker='o',
            markersize=8, markerfacecolor=COLORS[1], markeredgecolor='white',
            markeredgewidth=2, zorder=5)
    ax.fill_between(range(len(labels)), values, alpha=0.15, color=COLORS[0])

    ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel(xlabel, fontsize=12, labelpad=10)
    ax.set_ylabel(ylabel, fontsize=12, labelpad=10)
    ax.grid(axis='both', alpha=0.2)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    return fig_to_base64(fig)


def create_pie_chart(data: dict, title: str) -> str:
    """Create a styled pie chart. Returns base64 image string."""
    setup_style()
    fig, ax = plt.subplots(figsize=(8, 8))

    labels = list(data.keys())
    values = list(data.values())

    wedges, texts, autotexts = ax.pie(
        values, labels=labels, colors=COLORS[:len(labels)],
        autopct='%1.1f%%', startangle=90, pctdistance=0.8,
        wedgeprops=dict(width=0.5, edgecolor=BG_COLOR, linewidth=2)
    )

    for text in texts:
        text.set_fontsize(11)
        text.set_color(TEXT_COLOR)
    for autotext in autotexts:
        autotext.set_fontsize(10)
        autotext.set_fontweight('bold')
        autotext.set_color('white')

    ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
    plt.tight_layout()

    return fig_to_base64(fig)


def create_horizontal_bar_chart(data: dict, title: str, xlabel: str = "") -> str:
    """Create a styled horizontal bar chart. Returns base64 image string."""
    setup_style()
    fig, ax = plt.subplots(figsize=(10, 6))

    labels = list(data.keys())
    values = list(data.values())

    bars = ax.barh(labels, values, color=COLORS[:len(labels)], height=0.6,
                   edgecolor='none', alpha=0.9)

    for bar, val in zip(bars, values):
        ax.text(bar.get_width() + max(values) * 0.02, bar.get_y() + bar.get_height() / 2.,
                f'{val:,.0f}' if isinstance(val, (int, float)) else str(val),
                ha='left', va='center', fontsize=10, fontweight='bold', color=TEXT_COLOR)

    ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel(xlabel, fontsize=12, labelpad=10)
    ax.grid(axis='x', alpha=0.2)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.invert_yaxis()
    plt.tight_layout()

    return fig_to_base64(fig)
