<template>
  <div class="row justify-content-center">
    <div class="col-8">
      <form name="editForm" role="form" novalidate v-on:submit.prevent="save()">
        <h2
          id="demoApp.country.home.createOrEditLabel"
          data-cy="CountryCreateUpdateHeading"
          v-text="$t('demoApp.country.home.createOrEditLabel')"
        >
          Create or edit a Country
        </h2>
        <div>
          <div class="form-group" v-if="country.id">
            <label for="id" v-text="$t('global.field.id')">ID</label>
            <input type="text" class="form-control" id="id" name="id" v-model="country.id" readonly />
          </div>
          <div class="form-group">
            <label class="form-control-label" v-text="$t('demoApp.country.countryName')" for="country-countryName">Country Name</label>
            <input
              type="text"
              class="form-control"
              name="countryName"
              id="country-countryName"
              data-cy="countryName"
              :class="{ valid: !$v.country.countryName.$invalid, invalid: $v.country.countryName.$invalid }"
              v-model="$v.country.countryName.$model"
            />
          </div>
          <div class="form-group">
            <label class="form-control-label" v-text="$t('demoApp.country.region')" for="country-region">Region</label>
            <select class="form-control" id="country-region" data-cy="region" name="region" v-model="country.region">
              <option v-bind:value="null"></option>
              <option
                v-bind:value="country.region && regionOption.id === country.region.id ? country.region : regionOption"
                v-for="regionOption in regions"
                :key="regionOption.id"
              >
                {{ regionOption.id }}
              </option>
            </select>
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
            :disabled="$v.country.$invalid || isSaving"
            class="btn btn-primary"
          >
            <font-awesome-icon icon="save"></font-awesome-icon>&nbsp;<span v-text="$t('entity.action.save')">Save</span>
          </button>
        </div>
      </form>
    </div>
  </div>
</template>
<script lang="ts" src="./country-update.component.ts"></script>
