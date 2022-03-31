package com.example.demo.repository;

import com.example.demo.domain.Job;
import java.util.List;
import java.util.Optional;
import javax.persistence.EntityManager;
import org.hibernate.annotations.QueryHints;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageImpl;

/**
 * Utility repository to load bag relationships based on https://vladmihalcea.com/hibernate-multiplebagfetchexception/
 */
public class JobRepositoryWithBagRelationshipsImpl implements JobRepositoryWithBagRelationships {

    @Autowired
    private EntityManager entityManager;

    @Override
    public Optional<Job> fetchBagRelationships(Optional<Job> job) {
        return job.map(this::fetchTasks);
    }

    @Override
    public Page<Job> fetchBagRelationships(Page<Job> jobs) {
        return new PageImpl<>(fetchBagRelationships(jobs.getContent()), jobs.getPageable(), jobs.getTotalElements());
    }

    @Override
    public List<Job> fetchBagRelationships(List<Job> jobs) {
        return Optional.of(jobs).map(this::fetchTasks).get();
    }

    Job fetchTasks(Job result) {
        return entityManager
            .createQuery("select job from Job job left join fetch job.tasks where job is :job", Job.class)
            .setParameter("job", result)
            .setHint(QueryHints.PASS_DISTINCT_THROUGH, false)
            .getSingleResult();
    }

    List<Job> fetchTasks(List<Job> jobs) {
        return entityManager
            .createQuery("select distinct job from Job job left join fetch job.tasks where job in :jobs", Job.class)
            .setParameter("jobs", jobs)
            .setHint(QueryHints.PASS_DISTINCT_THROUGH, false)
            .getResultList();
    }
}
