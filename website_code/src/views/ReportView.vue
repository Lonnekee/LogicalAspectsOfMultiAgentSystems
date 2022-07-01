<template>
  <div class="report">
    <iframe class="pdf" width="100%" height="100%"
            :src=reportURL>
    </iframe>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      report: null,
      reportURL: "https://lonnekee.github.io/LogicalAspectsOfMultiAgentSystems/report.pdf"
    }
  },
  mounted() {
    axios.get(this.reportURL)
        .then(response => this.report = response)
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
