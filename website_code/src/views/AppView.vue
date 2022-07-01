<template>
  <div class="application">
    <h1>This is the page that will host the application.</h1>

    <script setup lang="ts">
      import {PythonShell} from 'python-shell';

      PythonShell.runString(
          'from tkinter import *; Tk().mainloop()',
          undefined,
          function(err: any) {
            if (err) throw err;
            console.log('finished');
          }
      )
    </script>
  </div>
</template>

<style>
@media (min-width: 1024px) {
  .application {
    min-height: 100vh;
    display: flex;
    align-items: center;
  }
}
</style>
