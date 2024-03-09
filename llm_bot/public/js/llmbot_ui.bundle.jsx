import * as React from "react";
import { App } from "./App";
import { createRoot } from "react-dom/client";
import { ChakraProvider } from "@chakra-ui/react";
import { extendTheme, withDefaultColorScheme } from "@chakra-ui/react";

const linkedinTheme = extendTheme(
  withDefaultColorScheme({ colorScheme: "linkedin" })
);

class llmBotUI {
  constructor({ wrapper, page }) {
    this.$wrapper = $(wrapper);
    this.page = page;
    this.init();
  }

  init() {
    const root = createRoot(this.$wrapper.get(0));
    root.render(
      <ChakraProvider theme={linkedinTheme}>
        <App />
      </ChakraProvider>
    );
  }
}

frappe.provide("llmbot.ui");
llmbot.ui.llmBotUI = llmBotUI;
export default llmBotUI;
