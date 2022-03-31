<template>
  <div class="row justify-content-center">
    <div class="col-8">
      <form name="editForm" role="form" novalidate v-on:submit.prevent="save()">
        <h2
          id="demoApp.employee.home.createOrEditLabel"
          data-cy="EmployeeCreateUpdateHeading"
          v-text="$t('demoApp.employee.home.createOrEditLabel')"
        >
          Create or edit a Employee
        </h2>
        <div>
          <div class="form-group" v-if="employee.id">
            <label for="id" v-text="$t('global.field.id')">ID</label>
            <input type="text" class="form-control" id="id" name="id" v-model="employee.id" readonly />
          </div>
          <div class="form-group">
            <label class="form-control-label" v-text="$t('demoApp.employee.firstName')" for="employee-firstName">First Name</label>
            <input
              type="text"
              class="form-control"
              name="firstName"
              id="employee-firstName"
              data-cy="firstName"
              :class="{ valid: !$v.employee.firstName.$invalid, invalid: $v.employee.firstName.$invalid }"
              v-model="$v.employee.firstName.$model"
            />
          </div>
          <div class="form-group">
            <label class="form-control-label" v-text="$t('demoApp.employee.lastName')" for="employee-lastName">Last Name</label>
            <input
              type="text"
              class="form-control"
              name="lastName"
              id="employee-lastName"
              data-cy="lastName"
              :class="{ valid: !$v.employee.lastName.$invalid, invalid: $v.employee.lastName.$invalid }"
              v-model="$v.employee.lastName.$model"
            />
          </div>
          <div class="form-group">
            <label class="form-control-label" v-text="$t('demoApp.employee.email')" for="employee-email">Email</label>
            <input
              type="text"
              class="form-control"
              name="email"
              id="employee-email"
              data-cy="email"
              :class="{ valid: !$v.employee.email.$invalid, invalid: $v.employee.email.$invalid }"
              v-model="$v.employee.email.$model"
            />
          </div>
          <div class="form-group">
            <label class="form-control-label" v-text="$t('demoApp.employee.phoneNumber')" for="employee-phoneNumber">Phone Number</label>
            <input
              type="text"
              class="form-control"
              name="phoneNumber"
              id="employee-phoneNumber"
              data-cy="phoneNumber"
              :class="{ valid: !$v.employee.phoneNumber.$invalid, invalid: $v.employee.phoneNumber.$invalid }"
              v-model="$v.employee.phoneNumber.$model"
            />
          </div>
          <div class="form-group">
            <label class="form-control-label" v-text="$t('demoApp.employee.hireDate')" for="employee-hireDate">Hire Date</label>
            <div class="d-flex">
              <input
                id="employee-hireDate"
                data-cy="hireDate"
                type="datetime-local"
                class="form-control"
                name="hireDate"
                :class="{ valid: !$v.employee.hireDate.$invalid, invalid: $v.employee.hireDate.$invalid }"
                :value="convertDateTimeFromServer($v.employee.hireDate.$model)"
                @change="updateInstantField('hireDate', $event)"
              />
            </div>
          </div>
          <div class="form-group">
            <label class="form-control-label" v-text="$t('demoApp.employee.salary')" for="employee-salary">Salary</label>
            <input
              type="number"
              class="form-control"
              name="salary"
              id="employee-salary"
              data-cy="salary"
              :class="{ valid: !$v.employee.salary.$invalid, invalid: $v.employee.salary.$invalid }"
              v-model.number="$v.employee.salary.$model"
            />
          </div>
          <div class="form-group">
            <label class="form-control-label" v-text="$t('demoApp.employee.commissionPct')" for="employee-commissionPct"
              >Commission Pct</label
            >
            <input
              type="number"
              class="form-control"
              name="commissionPct"
              id="employee-commissionPct"
              data-cy="commissionPct"
              :class="{ valid: !$v.employee.commissionPct.$invalid, invalid: $v.employee.commissionPct.$invalid }"
              v-model.number="$v.employee.commissionPct.$model"
            />
          </div>
          <div class="form-group">
            <label class="form-control-label" v-text="$t('demoApp.employee.manager')" for="employee-manager">Manager</label>
            <select class="form-control" id="employee-manager" data-cy="manager" name="manager" v-model="employee.manager">
              <option v-bind:value="null"></option>
              <option
                v-bind:value="employee.manager && employeeOption.id === employee.manager.id ? employee.manager : employeeOption"
                v-for="employeeOption in employees"
                :key="employeeOption.id"
              >
                {{ employeeOption.id }}
              </option>
            </select>
          </div>
          <div class="form-group">
            <label class="form-control-label" v-text="$t('demoApp.employee.department')" for="employee-department">Department</label>
            <select class="form-control" id="employee-department" data-cy="department" name="department" v-model="employee.department">
              <option v-bind:value="null"></option>
              <option
                v-bind:value="
                  employee.department && departmentOption.id === employee.department.id ? employee.department : departmentOption
                "
                v-for="departmentOption in departments"
                :key="departmentOption.id"
              >
                {{ departmentOption.id }}
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
            :disabled="$v.employee.$invalid || isSaving"
            class="btn btn-primary"
          >
            <font-awesome-icon icon="save"></font-awesome-icon>&nbsp;<span v-text="$t('entity.action.save')">Save</span>
          </button>
        </div>
      </form>
    </div>
  </div>
</template>
<script lang="ts" src="./employee-update.component.ts"></script>
