import Alpine from "alpinejs";
import htmx from "htmx.org";
import focus from "@alpinejs/focus";

// global HTMX configuration
// https://htmx.org/docs/#config

htmx.config.historyCacheSize = 0;
htmx.config.refreshOnHistoryMiss = false;
htmx.config.useTemplateFragments = true;

// set global Alpine instance
window.Alpine = Alpine;

Alpine.plugin(focus);
Alpine.start();
