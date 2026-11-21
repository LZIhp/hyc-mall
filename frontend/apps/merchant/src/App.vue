<template>
  <router-view />
</template>

<style>
@import '@hyc/ui/tokens.css';

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: var(--hyc-font-body);
  background: var(--hyc-cream);
  color: var(--hyc-ink);
  -webkit-font-smoothing: antialiased;
}
</style>
