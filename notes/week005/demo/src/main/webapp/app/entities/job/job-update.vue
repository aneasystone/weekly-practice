<template>
  <div class="row justify-content-center">
    <div class="col-8">
      <form name="editForm" role="form" novalidate v-on:submit.prevent="save()">
        <h2 id="demoApp.job.home.createOrEditLabel" data-cy="JobCreateUpdateHeading" v-text="$t('demoApp.job.home.createOrEditLabel')">
          Create or edit a Job
        </h2>
        <div>
          <div class="form-group" v-if="job.id">
            <label for="id" v-text="$t('global.field.id')">ID</label>
            <input type="text" class="form-control" id="id" name="id" v-model="job.id" readonly />
          </div>
          <div class="form-group">
            <label class="form-control-label" v-text="$t('demoApp.job.jobTitle')" for="job-jobTitle">Job Title</label>
            <input
              type="text"
              class="form-control"
              name="jobTitle"
              id="job-jobTitle"
              data-cy="jobTitle"
              :class="{ valid: !$v.job.jobTitle.$invalid, invalid: $v.job.jobTitle.$invalid }"
              v-model="$v.job.jobTitle.$model"
            />
          </div>
          <div class="form-group">
            <label class="form-control-label" v-text="$t('demoApp.job.minSalary')" for="job-minSalary">Min Salary</label>
            <input
              type="number"
              class="form-control"
              name="minSalary"
              id="job-minSalary"
              data-cy="minSalary"
              :class="{ valid: !$v.job.minSalary.$invalid, invalid: $v.job.minSalary.$invalid }"
              v-model.number="$v.job.minSalary.$model"
            />
          </div>
          <div class="form-group">
            <label class="form-control-label" v-text="$t('demoApp.job.maxSalary')" for="job-maxSalary">Max Salary</label>
            <input
              type="number"
              class="form-control"
              name="maxSalary"
              id="job-maxSalary"
              data-cy="maxSalary"
              :class="{ valid: !$v.job.maxSalary.$invalid, invalid: $v.job.maxSalary.$invalid }"
              v-model.number="$v.job.maxSalary.$model"
            />
          </div>
          <div class="form-group">
            <label v-text="$t('demoApp.job.task')" for="job-task">Task</label>
            <select
              class="form-control"
              id="job-tasks"
              data-cy="task"
              multiple
              name="task"
              v-if="job.tasks !== undefined"
              v-model="job.tasks"
            >
              <option v-bind:value="getSelected(job.tasks, taskOption)" v-for="taskOption in tasks" :key="taskOption.id">
                {{ taskOption.title }}
              </option>
            </select>
          </div>
          <div class="form-group">
            <label class="form-control-label" v-text="$t('demoApp.job.employee')" for="job-employee">Employee</label>
            <select class="form-control" id="job-employee" data-cy="employee" name="employee" v-model="job.employee">
              <option v-bind:value="null"></option>
              <option
                v-bind:value="job.employee && employeeOption.id === job.employee.id ? job.employee : employeeOption"
                v-for="employeeOption in employees"
                :key="employeeOption.id"
              >
                {{ employeeOption.id }}
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
            :disabled="$v.job.$invalid || isSaving"
            class="btn btn-primary"
          >
            <font-awesome-icon icon="save"></font-awesome-icon>&nbsp;<span v-text="$t('entity.action.save')">Save</span>
          </button>
        </div>
      </form>
    </div>
  </div>
</template>
<script lang="ts" src="./job-update.component.ts"></script>
