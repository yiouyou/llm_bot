frappe.ui.keys.add_shortcut({
  shortcut: "shift+ctrl+d",
  action: function () {
    // navigate to LLM Bot page
    frappe.set_route("llm-bot");
  },
  description: __("LLM Bot"),
});
