<template>
  <div class="report">
    <iframe class="pdf" width="100%" height="100%"
            :src="reportURL">
    </iframe>
  </div>
</template>

<script>
export default {
  data() {
    return {
      reportURL: "https://lonnekee.github.io/LogicalAspectsOfMultiAgentSystems/report.pdf"
    }
  }
}
</script>

<style>
@media (min-width: 1024px) {
  .report {
    min-height: 100vh;
    display: flex;
    align-items: center;
  }

  .pdf {
    height: 900px;
  }
}

@media (max-width: 1024px) {
  .pdf {
    height: 100%;
  }
}
</style>
