frappe.ui.keys.add_shortcut({
  shortcut: "shift+ctrl+d",
  action: function () {
    // navigate to ask llm bot page
    frappe.set_route("llm-bot");
  },
  description: __("Ask llmBot"),
});
