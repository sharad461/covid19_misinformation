
import textwrap
import plotly.express as px
import matplotlib.text as mpl_text

def wrap_labels(ax, width, break_long_words=False):
    labels = []
    for label in ax.get_yticklabels():
        text = label.get_text()
        labels.append(
            textwrap.fill(text, width=width, break_long_words=break_long_words)
        )
    ax.set_yticklabels(labels, rotation=0)


def generate_and_save_fig(table, type_column, title):
    # fig, ax = plt.subplots(figsize=(8, 6))

    # order = table.sort_values(by="Frequency", ascending=False)

    # ax = sns.barplot(
    #     y=type_column, x="Frequency", data=table, order=order[type_column]
    # )

    # ax.bar_label(ax.containers[0])
    # wrap_labels(ax, 10)

    # colors = sns.color_palette()
    # pie = plt.pie(table.Frequency, colors=colors)

    # labels = [l for l in zip(table[type_column], )]
    # labels = ["\n".join(textwrap.wrap(l, 35)) for l in table[type_column]]

    # plt.legend(
    #     pie[0],
    #     labels,
    #     bbox_to_anchor=(1, 0.5),
    #     bbox_transform=plt.gcf().transFigure,
    #     loc="center right",
    #     fontsize=10,
    # )
    # plt.subplots_adjust(left=0.0, bottom=0.1, right=0.7)

    # pie = plt.pie(table.Frequency, colors=colors)

    table["labels"] = [
        "<br>".join(textwrap.wrap(l, 40)) for l in table[type_column]
    ]

    fig = px.pie(
        table,
        values="Frequency",
        names="labels",
        title=title,
    )

    fig.update_layout(
        legend={
            "yanchor": "middle",
            "y": 0.54,
            "x": 1.15,
            "xanchor": "right",
        },
        title={
            "x": 0.5,
            "xanchor": "center",
            "yanchor": "top",
        },
    )

    fig.show()


class AnyObject(object):
    def __init__(self, text, color):
        self.my_text = text
        self.my_color = color


class AnyObjectHandler(object):
    def legend_artist(self, legend, orig_handle, fontsize, handlebox):
        x0, y0 = handlebox.xdescent, handlebox.ydescent
        width, height = handlebox.width, handlebox.height
        patch = mpl_text.Text(
            x=0,
            y=0,
            text=orig_handle.my_text,
            color=orig_handle.my_color,
            verticalalignment="baseline",
            horizontalalignment="left",
            multialignment=None,
            fontproperties=None,
            rotation=0,
            linespacing=None,
            rotation_mode=None,
        )
        handlebox.add_artist(patch)
        return patch
