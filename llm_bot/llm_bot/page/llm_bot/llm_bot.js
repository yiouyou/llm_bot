frappe.pages['llm-bot'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'LLM Bot',
		single_column: true
	});
}

frappe.pages["llm-bot"].on_page_show = function (wrapper) {
  load_askllm_ui(wrapper);
};

function load_askllm_ui(wrapper) {
  let $parent = $(wrapper).find(".layout-main-section");
  $parent.empty();

  frappe.require("llmbot_ui.bundle.jsx").then(() => {
    new llmbot.ui.llmBotUI({
      wrapper: $parent,
      page: wrapper.page,
    });
  });
}
