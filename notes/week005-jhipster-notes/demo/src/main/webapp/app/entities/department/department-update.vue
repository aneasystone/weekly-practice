<template>
  <div class="row justify-content-center">
    <div class="col-8">
      <form name="editForm" role="form" novalidate v-on:submit.prevent="save()">
        <h2
          id="demoApp.department.home.createOrEditLabel"
          data-cy="DepartmentCreateUpdateHeading"
          v-text="$t('demoApp.department.home.createOrEditLabel')"
        >
          Create or edit a Department
        </h2>
        <div>
          <div class="form-group" v-if="department.id">
            <label for="id" v-text="$t('global.field.id')">ID</label>
            <input type="text" class="form-control" id="id" name="id" v-model="department.id" readonly />
          </div>
          <div class="form-group">
            <label class="form-control-label" v-text="$t('demoApp.department.departmentName')" for="department-departmentName"
              >Department Name</label
            >
            <input
              type="text"
              class="form-control"
              name="departmentName"
              id="department-departmentName"
              data-cy="departmentName"
              :class="{ valid: !$v.department.departmentName.$invalid, invalid: $v.department.departmentName.$invalid }"
              v-model="$v.department.departmentName.$model"
              required
            />
            <div v-if="$v.department.departmentName.$anyDirty && $v.department.departmentName.$invalid">
              <small class="form-text text-danger" v-if="!$v.department.departmentName.required" v-text="$t('entity.validation.required')">
                This field is required.
              </small>
            </div>
          </div>
          <div class="form-group">
            <label class="form-control-label" v-text="$t('demoApp.department.location')" for="department-location">Location</label>
            <select class="form-control" id="department-location" data-cy="location" name="location" v-model="department.location">
              <option v-bind:value="null"></option>
              <option
                v-bind:value="department.location && locationOption.id === department.location.id ? department.location : locationOption"
                v-for="locationOption in locations"
                :key="locationOption.id"
              >
                {{ locationOption.id }}
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
            :disabled="$v.department.$invalid || isSaving"
            class="btn btn-primary"
          >
            <font-awesome-icon icon="save"></font-awesome-icon>&nbsp;<span v-text="$t('entity.action.save')">Save</span>
          </button>
        </div>
      </form>
    </div>
  </div>
</template>
<script lang="ts" src="./department-update.component.ts"></script>
