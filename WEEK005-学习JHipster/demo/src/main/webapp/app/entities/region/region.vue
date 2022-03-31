<template>
  <div>
    <h2 id="page-heading" data-cy="RegionHeading">
      <span v-text="$t('demoApp.region.home.title')" id="region-heading">Regions</span>
      <div class="d-flex justify-content-end">
        <button class="btn btn-info mr-2" v-on:click="handleSyncList" :disabled="isFetching">
          <font-awesome-icon icon="sync" :spin="isFetching"></font-awesome-icon>
          <span v-text="$t('demoApp.region.home.refreshListLabel')">Refresh List</span>
        </button>
        <router-link :to="{ name: 'RegionCreate' }" custom v-slot="{ navigate }">
          <button
            @click="navigate"
            id="jh-create-entity"
            data-cy="entityCreateButton"
            class="btn btn-primary jh-create-entity create-region"
          >
            <font-awesome-icon icon="plus"></font-awesome-icon>
            <span v-text="$t('demoApp.region.home.createLabel')"> Create a new Region </span>
          </button>
        </router-link>
      </div>
    </h2>
    <br />
    <div class="alert alert-warning" v-if="!isFetching && regions && regions.length === 0">
      <span v-text="$t('demoApp.region.home.notFound')">No regions found</span>
    </div>
    <div class="table-responsive" v-if="regions && regions.length > 0">
      <table class="table table-striped" aria-describedby="regions">
        <thead>
          <tr>
            <th scope="row"><span v-text="$t('global.field.id')">ID</span></th>
            <th scope="row"><span v-text="$t('demoApp.region.regionName')">Region Name</span></th>
            <th scope="row"></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="region in regions" :key="region.id" data-cy="entityTable">
            <td>
              <router-link :to="{ name: 'RegionView', params: { regionId: region.id } }">{{ region.id }}</router-link>
            </td>
            <td>{{ region.regionName }}</td>
            <td class="text-right">
              <div class="btn-group">
                <router-link :to="{ name: 'RegionView', params: { regionId: region.id } }" custom v-slot="{ navigate }">
                  <button @click="navigate" class="btn btn-info btn-sm details" data-cy="entityDetailsButton">
                    <font-awesome-icon icon="eye"></font-awesome-icon>
                    <span class="d-none d-md-inline" v-text="$t('entity.action.view')">View</span>
                  </button>
                </router-link>
                <router-link :to="{ name: 'RegionEdit', params: { regionId: region.id } }" custom v-slot="{ navigate }">
                  <button @click="navigate" class="btn btn-primary btn-sm edit" data-cy="entityEditButton">
                    <font-awesome-icon icon="pencil-alt"></font-awesome-icon>
                    <span class="d-none d-md-inline" v-text="$t('entity.action.edit')">Edit</span>
                  </button>
                </router-link>
                <b-button
                  v-on:click="prepareRemove(region)"
                  variant="danger"
                  class="btn btn-sm"
                  data-cy="entityDeleteButton"
                  v-b-modal.removeEntity
                >
                  <font-awesome-icon icon="times"></font-awesome-icon>
                  <span class="d-none d-md-inline" v-text="$t('entity.action.delete')">Delete</span>
                </b-button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <b-modal ref="removeEntity" id="removeEntity">
      <span slot="modal-title"
        ><span id="demoApp.region.delete.question" data-cy="regionDeleteDialogHeading" v-text="$t('entity.delete.title')"
          >Confirm delete operation</span
        ></span
      >
      <div class="modal-body">
        <p id="jhi-delete-region-heading" v-text="$t('demoApp.region.delete.question', { id: removeId })">
          Are you sure you want to delete this Region?
        </p>
      </div>
      <div slot="modal-footer">
        <button type="button" class="btn btn-secondary" v-text="$t('entity.action.cancel')" v-on:click="closeDialog()">Cancel</button>
        <button
          type="button"
          class="btn btn-primary"
          id="jhi-confirm-delete-region"
          data-cy="entityConfirmDeleteButton"
          v-text="$t('entity.action.delete')"
          v-on:click="removeRegion()"
        >
          Delete
        </button>
      </div>
    </b-modal>
  </div>
</template>

<script lang="ts" src="./region.component.ts"></script>
