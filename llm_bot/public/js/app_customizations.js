frappe.ui.keys.add_shortcut({
  shortcut: "shift+ctrl+d",
  action: function () {
    // navigate to ask llm page
    frappe.set_route("ask-llm");
  },
  description: __("Ask LLM"),
});
