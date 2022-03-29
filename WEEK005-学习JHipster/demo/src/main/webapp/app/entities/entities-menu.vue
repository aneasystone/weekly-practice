<template>
  <div>
    <b-dropdown-item to="/foo">
      <font-awesome-icon icon="asterisk" />
      <span v-text="$t('global.menu.entities.foo')">Foo</span>
    </b-dropdown-item>
    <!-- jhipster-needle-add-entity-to-menu - JHipster will add entities to the menu here -->
  </div>
</template>

<script lang="ts" src="./entities-menu.component.ts"></script>
