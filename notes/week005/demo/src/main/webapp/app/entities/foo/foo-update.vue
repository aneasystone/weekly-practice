<template>
  <div class="row justify-content-center">
    <div class="col-8">
      <form name="editForm" role="form" novalidate v-on:submit.prevent="save()">
        <h2 id="demoApp.foo.home.createOrEditLabel" data-cy="FooCreateUpdateHeading" v-text="$t('demoApp.foo.home.createOrEditLabel')">
          Create or edit a Foo
        </h2>
        <div>
          <div class="form-group" v-if="foo.id">
            <label for="id" v-text="$t('global.field.id')">ID</label>
            <input type="text" class="form-control" id="id" name="id" v-model="foo.id" readonly />
          </div>
          <div class="form-group">
            <label class="form-control-label" v-text="$t('demoApp.foo.name')" for="foo-name">Name</label>
            <input
              type="text"
              class="form-control"
              name="name"
              id="foo-name"
              data-cy="name"
              :class="{ valid: !$v.foo.name.$invalid, invalid: $v.foo.name.$invalid }"
              v-model="$v.foo.name.$model"
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
            :disabled="$v.foo.$invalid || isSaving"
            class="btn btn-primary"
          >
            <font-awesome-icon icon="save"></font-awesome-icon>&nbsp;<span v-text="$t('entity.action.save')">Save</span>
          </button>
        </div>
      </form>
    </div>
  </div>
</template>
<script lang="ts" src="./foo-update.component.ts"></script>
