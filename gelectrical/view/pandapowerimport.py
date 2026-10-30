"""Read-only GTK viewer for imported Pandapower networks."""

from gi.repository import Gtk

from ..model.pandapower_import import NETWORK_TABLES, summarize_network


MAX_DISPLAY_ROWS = 1000


class PandapowerImportDialog:
    """Display imported Pandapower element tables without editing the network."""

    def __init__(self, parent, network, filename):
        self.dialog = Gtk.Dialog(
            title="Imported Pandapower Network",
            transient_for=parent,
            flags=Gtk.DialogFlags.MODAL | Gtk.DialogFlags.DESTROY_WITH_PARENT,
        )
        self.dialog.set_default_size(1050, 680)
        self.dialog.add_button(Gtk.STOCK_CLOSE, Gtk.ResponseType.CLOSE)

        content = self.dialog.get_content_area()
        content.set_spacing(8)
        content.set_border_width(10)

        heading = Gtk.Label()
        heading.set_markup("<b>{}</b>".format(GLibMarkup.escape(filename)))
        heading.set_xalign(0)
        content.pack_start(heading, False, False, 0)

        summary = Gtk.Label(label=summarize_network(network))
        summary.set_xalign(0)
        summary.set_selectable(True)
        content.pack_start(summary, False, False, 0)

        notebook = Gtk.Notebook()
        notebook.set_scrollable(True)
        content.pack_start(notebook, True, True, 0)

        for table_name, label in NETWORK_TABLES:
            table = network.get(table_name)
            if table is None or len(table.index) == 0:
                continue
            page, count = self._build_table_page(table)
            tab_label = Gtk.Label(label="{} ({})".format(label, len(table.index)))
            notebook.append_page(page, tab_label)
            if len(table.index) > count:
                page.set_tooltip_text(
                    "Showing the first {} of {} rows.".format(count, len(table.index)))

        if notebook.get_n_pages() == 0:
            empty = Gtk.Label(label="No supported network elements were found.")
            empty.set_margin_top(24)
            notebook.append_page(empty, Gtk.Label(label="Network"))

        self.dialog.show_all()

    def _build_table_page(self, table):
        columns = [str(column) for column in table.columns]
        model = Gtk.ListStore(*([str] * (len(columns) + 1)))
        display_table = table.head(MAX_DISPLAY_ROWS)

        for index, row in display_table.iterrows():
            values = [str(index)]
            for value in row.tolist():
                if value is None:
                    values.append("")
                else:
                    try:
                        values.append("" if value != value else str(value))
                    except Exception:
                        values.append(str(value))
            model.append(values)

        tree = Gtk.TreeView(model=model)
        tree.set_enable_search(True)
        tree.set_search_column(0)
        tree.set_rules_hint(True)

        index_renderer = Gtk.CellRendererText()
        index_column = Gtk.TreeViewColumn("Index", index_renderer, text=0)
        index_column.set_resizable(True)
        index_column.set_min_width(70)
        tree.append_column(index_column)

        for position, title in enumerate(columns, start=1):
            renderer = Gtk.CellRendererText()
            renderer.set_property("ellipsize", 3)
            column = Gtk.TreeViewColumn(title, renderer, text=position)
            column.set_resizable(True)
            column.set_min_width(100)
            tree.append_column(column)

        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scrolled.add(tree)
        return scrolled, len(display_table)

    def run(self):
        try:
            return self.dialog.run()
        finally:
            self.dialog.destroy()


class GLibMarkup:
    """Minimal markup escaping for labels populated from file names."""

    @staticmethod
    def escape(value):
        return (str(value).replace("&", "&amp;")
                .replace("<", "&lt;").replace(">", "&gt;")
                .replace('"', "&quot;").replace("'", "&apos;"))
