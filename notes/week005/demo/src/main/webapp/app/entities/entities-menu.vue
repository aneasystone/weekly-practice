<template>
  <div>
    <b-dropdown-item to="/foo">
      <font-awesome-icon icon="asterisk" />
      <span v-text="$t('global.menu.entities.foo')">Foo</span>
    </b-dropdown-item>
    <b-dropdown-item to="/region">
      <font-awesome-icon icon="asterisk" />
      <span v-text="$t('global.menu.entities.region')">Region</span>
    </b-dropdown-item>
    <b-dropdown-item to="/country">
      <font-awesome-icon icon="asterisk" />
      <span v-text="$t('global.menu.entities.country')">Country</span>
    </b-dropdown-item>
    <b-dropdown-item to="/location">
      <font-awesome-icon icon="asterisk" />
      <span v-text="$t('global.menu.entities.location')">Location</span>
    </b-dropdown-item>
    <b-dropdown-item to="/department">
      <font-awesome-icon icon="asterisk" />
      <span v-text="$t('global.menu.entities.department')">Department</span>
    </b-dropdown-item>
    <b-dropdown-item to="/task">
      <font-awesome-icon icon="asterisk" />
      <span v-text="$t('global.menu.entities.task')">Task</span>
    </b-dropdown-item>
    <b-dropdown-item to="/employee">
      <font-awesome-icon icon="asterisk" />
      <span v-text="$t('global.menu.entities.employee')">Employee</span>
    </b-dropdown-item>
    <b-dropdown-item to="/job">
      <font-awesome-icon icon="asterisk" />
      <span v-text="$t('global.menu.entities.job')">Job</span>
    </b-dropdown-item>
    <b-dropdown-item to="/job-history">
      <font-awesome-icon icon="asterisk" />
      <span v-text="$t('global.menu.entities.jobHistory')">Job History</span>
    </b-dropdown-item>
    <!-- jhipster-needle-add-entity-to-menu - JHipster will add entities to the menu here -->
  </div>
</template>

<script lang="ts" src="./entities-menu.component.ts"></script>
