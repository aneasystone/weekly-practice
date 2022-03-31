<template>
  <div class="row justify-content-center">
    <div class="col-8">
      <form name="editForm" role="form" novalidate v-on:submit.prevent="save()">
        <h2
          id="demoApp.region.home.createOrEditLabel"
          data-cy="RegionCreateUpdateHeading"
          v-text="$t('demoApp.region.home.createOrEditLabel')"
        >
          Create or edit a Region
        </h2>
        <div>
          <div class="form-group" v-if="region.id">
            <label for="id" v-text="$t('global.field.id')">ID</label>
            <input type="text" class="form-control" id="id" name="id" v-model="region.id" readonly />
          </div>
          <div class="form-group">
            <label class="form-control-label" v-text="$t('demoApp.region.regionName')" for="region-regionName">Region Name</label>
            <input
              type="text"
              class="form-control"
              name="regionName"
              id="region-regionName"
              data-cy="regionName"
              :class="{ valid: !$v.region.regionName.$invalid, invalid: $v.region.regionName.$invalid }"
              v-model="$v.region.regionName.$model"
            />
          </div>
        </div>
        <div>
          <button type="button" id="cancel-save" data-cy="entityCreateCancelButton" class="btn btn-secondary" v-on:click="previousState()">
            <font-awesome-icon icon="ban"></font-awesome-icon>&nbsp;<span v-text="$t('entity.action.cancel')">Cancel</span>
          </button>
          <button
            type="submit"
            id="save-entity"
            data-cy="entityCreateSaveButton"
            :disabled="$v.region.$invalid || isSaving"
            class="btn btn-primary"
          >
            <font-awesome-icon icon="save"></font-awesome-icon>&nbsp;<span v-text="$t('entity.action.save')">Save</span>
          </button>
        </div>
      </form>
    </div>
  </div>
</template>
<script lang="ts" src="./region-update.component.ts"></script>
