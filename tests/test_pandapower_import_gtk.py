"""Headless GTK smoke tests for the Pandapower import dialog."""

import importlib
import os
import sys
import types
import unittest

os.environ.setdefault("GDK_BACKEND", "x11")

try:
    import gi
    gi.require_version("Gtk", "3.0")
    from gi.repository import Gtk
except (ImportError, ValueError):
    Gtk = None


@unittest.skipIf(Gtk is None, "GTK 3 introspection bindings are unavailable")
class PandapowerImportGtkTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import pandas as pd

        package = types.ModuleType("gelectrical")
        package.__path__ = [os.path.abspath("gelectrical")]
        sys.modules.setdefault("gelectrical", package)
        model_package = types.ModuleType("gelectrical.model")
        model_package.__path__ = [os.path.abspath("gelectrical/model")]
        sys.modules.setdefault("gelectrical.model", model_package)
        view_package = types.ModuleType("gelectrical.view")
        view_package.__path__ = [os.path.abspath("gelectrical/view")]
        sys.modules.setdefault("gelectrical.view", view_package)

        cls.module = importlib.import_module("gelectrical.view.pandapowerimport")
        cls.pd = pd

    def setUp(self):
        self.network = {
            "bus": self.pd.DataFrame({"vn_kv": [0.4], "name": ["Bus A"]}),
            "line": self.pd.DataFrame({"length_km": [1.0]}),
            "res_bus": self.pd.DataFrame({"vm_pu": [1.0], "va_degree": [0.0]}),
            "res_line": self.pd.DataFrame({"loading_percent": [12.5]}),
        }

    def test_dialog_builds_network_tables_and_powerflow_control(self):
        dialog = self.module.PandapowerImportDialog(None, self.network, "sample.json")
        try:
            self.assertEqual(dialog.notebook.get_n_pages(), 2)
            self.assertEqual(dialog.run_button.get_label(), "Run Balanced Power Flow")
            self.assertTrue(dialog.run_button.get_sensitive())
            self.assertIn("Buses: 1", self.module.summarize_network(self.network))
        finally:
            dialog.dialog.destroy()

    def test_result_tables_are_added_and_refreshable(self):
        dialog = self.module.PandapowerImportDialog(None, self.network, "sample.json")
        try:
            dialog._show_powerflow_results()
            self.assertEqual(dialog.notebook.get_n_pages(), 4)
            first_pages = dict(dialog.result_pages)
            dialog._show_powerflow_results()
            self.assertEqual(dialog.notebook.get_n_pages(), 4)
            self.assertEqual(set(dialog.result_pages), set(first_pages))
        finally:
            dialog.dialog.destroy()

    def test_filename_markup_is_escaped(self):
        self.assertEqual(
            self.module.GLibMarkup.escape("network<&>.json"),
            "network&lt;&amp;&gt;.json",
        )


if __name__ == "__main__":
    unittest.main()
