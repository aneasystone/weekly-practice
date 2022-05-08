<template>
  <div>
    <h2 id="page-heading" data-cy="JobHeading">
      <span v-text="$t('demoApp.job.home.title')" id="job-heading">Jobs</span>
      <div class="d-flex justify-content-end">
        <button class="btn btn-info mr-2" v-on:click="handleSyncList" :disabled="isFetching">
          <font-awesome-icon icon="sync" :spin="isFetching"></font-awesome-icon>
          <span v-text="$t('demoApp.job.home.refreshListLabel')">Refresh List</span>
        </button>
        <router-link :to="{ name: 'JobCreate' }" custom v-slot="{ navigate }">
          <button @click="navigate" id="jh-create-entity" data-cy="entityCreateButton" class="btn btn-primary jh-create-entity create-job">
            <font-awesome-icon icon="plus"></font-awesome-icon>
            <span v-text="$t('demoApp.job.home.createLabel')"> Create a new Job </span>
          </button>
        </router-link>
      </div>
    </h2>
    <br />
    <div class="alert alert-warning" v-if="!isFetching && jobs && jobs.length === 0">
      <span v-text="$t('demoApp.job.home.notFound')">No jobs found</span>
    </div>
    <div class="table-responsive" v-if="jobs && jobs.length > 0">
      <table class="table table-striped" aria-describedby="jobs">
        <thead>
          <tr>
            <th scope="row" v-on:click="changeOrder('id')">
              <span v-text="$t('global.field.id')">ID</span>
              <jhi-sort-indicator :current-order="propOrder" :reverse="reverse" :field-name="'id'"></jhi-sort-indicator>
            </th>
            <th scope="row" v-on:click="changeOrder('jobTitle')">
              <span v-text="$t('demoApp.job.jobTitle')">Job Title</span>
              <jhi-sort-indicator :current-order="propOrder" :reverse="reverse" :field-name="'jobTitle'"></jhi-sort-indicator>
            </th>
            <th scope="row" v-on:click="changeOrder('minSalary')">
              <span v-text="$t('demoApp.job.minSalary')">Min Salary</span>
              <jhi-sort-indicator :current-order="propOrder" :reverse="reverse" :field-name="'minSalary'"></jhi-sort-indicator>
            </th>
            <th scope="row" v-on:click="changeOrder('maxSalary')">
              <span v-text="$t('demoApp.job.maxSalary')">Max Salary</span>
              <jhi-sort-indicator :current-order="propOrder" :reverse="reverse" :field-name="'maxSalary'"></jhi-sort-indicator>
            </th>
            <th scope="row" v-on:click="changeOrder('employee.id')">
              <span v-text="$t('demoApp.job.employee')">Employee</span>
              <jhi-sort-indicator :current-order="propOrder" :reverse="reverse" :field-name="'employee.id'"></jhi-sort-indicator>
            </th>
            <th scope="row"></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="job in jobs" :key="job.id" data-cy="entityTable">
            <td>
              <router-link :to="{ name: 'JobView', params: { jobId: job.id } }">{{ job.id }}</router-link>
            </td>
            <td>{{ job.jobTitle }}</td>
            <td>{{ job.minSalary }}</td>
            <td>{{ job.maxSalary }}</td>
            <td>
              <div v-if="job.employee">
                <router-link :to="{ name: 'EmployeeView', params: { employeeId: job.employee.id } }">{{ job.employee.id }}</router-link>
              </div>
            </td>
            <td class="text-right">
              <div class="btn-group">
                <router-link :to="{ name: 'JobView', params: { jobId: job.id } }" custom v-slot="{ navigate }">
                  <button @click="navigate" class="btn btn-info btn-sm details" data-cy="entityDetailsButton">
                    <font-awesome-icon icon="eye"></font-awesome-icon>
                    <span class="d-none d-md-inline" v-text="$t('entity.action.view')">View</span>
                  </button>
                </router-link>
                <router-link :to="{ name: 'JobEdit', params: { jobId: job.id } }" custom v-slot="{ navigate }">
                  <button @click="navigate" class="btn btn-primary btn-sm edit" data-cy="entityEditButton">
                    <font-awesome-icon icon="pencil-alt"></font-awesome-icon>
                    <span class="d-none d-md-inline" v-text="$t('entity.action.edit')">Edit</span>
                  </button>
                </router-link>
                <b-button
                  v-on:click="prepareRemove(job)"
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
        ><span id="demoApp.job.delete.question" data-cy="jobDeleteDialogHeading" v-text="$t('entity.delete.title')"
          >Confirm delete operation</span
        ></span
      >
      <div class="modal-body">
        <p id="jhi-delete-job-heading" v-text="$t('demoApp.job.delete.question', { id: removeId })">
          Are you sure you want to delete this Job?
        </p>
      </div>
      <div slot="modal-footer">
        <button type="button" class="btn btn-secondary" v-text="$t('entity.action.cancel')" v-on:click="closeDialog()">Cancel</button>
        <button
          type="button"
          class="btn btn-primary"
          id="jhi-confirm-delete-job"
          data-cy="entityConfirmDeleteButton"
          v-text="$t('entity.action.delete')"
          v-on:click="removeJob()"
        >
          Delete
        </button>
      </div>
    </b-modal>
    <div v-show="jobs && jobs.length > 0">
      <div class="row justify-content-center">
        <jhi-item-count :page="page" :total="queryCount" :itemsPerPage="itemsPerPage"></jhi-item-count>
      </div>
      <div class="row justify-content-center">
        <b-pagination size="md" :total-rows="totalItems" v-model="page" :per-page="itemsPerPage" :change="loadPage(page)"></b-pagination>
      </div>
    </div>
  </div>
</template>

<script lang="ts" src="./job.component.ts"></script>
