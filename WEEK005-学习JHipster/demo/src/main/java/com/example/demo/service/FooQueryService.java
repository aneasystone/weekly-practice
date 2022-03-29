package com.example.demo.service;

import com.example.demo.domain.*; // for static metamodels
import com.example.demo.domain.Foo;
import com.example.demo.repository.FooRepository;
import com.example.demo.service.criteria.FooCriteria;
import com.example.demo.service.dto.FooDTO;
import com.example.demo.service.mapper.FooMapper;
import java.util.List;
import javax.persistence.criteria.JoinType;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.domain.Specification;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import tech.jhipster.service.QueryService;

/**
 * Service for executing complex queries for {@link Foo} entities in the database.
 * The main input is a {@link FooCriteria} which gets converted to {@link Specification},
 * in a way that all the filters must apply.
 * It returns a {@link List} of {@link FooDTO} or a {@link Page} of {@link FooDTO} which fulfills the criteria.
 */
@Service
@Transactional(readOnly = true)
public class FooQueryService extends QueryService<Foo> {

    private final Logger log = LoggerFactory.getLogger(FooQueryService.class);

    private final FooRepository fooRepository;

    private final FooMapper fooMapper;

    public FooQueryService(FooRepository fooRepository, FooMapper fooMapper) {
        this.fooRepository = fooRepository;
        this.fooMapper = fooMapper;
    }

    /**
     * Return a {@link List} of {@link FooDTO} which matches the criteria from the database.
     * @param criteria The object which holds all the filters, which the entities should match.
     * @return the matching entities.
     */
    @Transactional(readOnly = true)
    public List<FooDTO> findByCriteria(FooCriteria criteria) {
        log.debug("find by criteria : {}", criteria);
        final Specification<Foo> specification = createSpecification(criteria);
        return fooMapper.toDto(fooRepository.findAll(specification));
    }

    /**
     * Return a {@link Page} of {@link FooDTO} which matches the criteria from the database.
     * @param criteria The object which holds all the filters, which the entities should match.
     * @param page The page, which should be returned.
     * @return the matching entities.
     */
    @Transactional(readOnly = true)
    public Page<FooDTO> findByCriteria(FooCriteria criteria, Pageable page) {
        log.debug("find by criteria : {}, page: {}", criteria, page);
        final Specification<Foo> specification = createSpecification(criteria);
        return fooRepository.findAll(specification, page).map(fooMapper::toDto);
    }

    /**
     * Return the number of matching entities in the database.
     * @param criteria The object which holds all the filters, which the entities should match.
     * @return the number of matching entities.
     */
    @Transactional(readOnly = true)
    public long countByCriteria(FooCriteria criteria) {
        log.debug("count by criteria : {}", criteria);
        final Specification<Foo> specification = createSpecification(criteria);
        return fooRepository.count(specification);
    }

    /**
     * Function to convert {@link FooCriteria} to a {@link Specification}
     * @param criteria The object which holds all the filters, which the entities should match.
     * @return the matching {@link Specification} of the entity.
     */
    protected Specification<Foo> createSpecification(FooCriteria criteria) {
        Specification<Foo> specification = Specification.where(null);
        if (criteria != null) {
            // This has to be called first, because the distinct method returns null
            if (criteria.getDistinct() != null) {
                specification = specification.and(distinct(criteria.getDistinct()));
            }
            if (criteria.getId() != null) {
                specification = specification.and(buildRangeSpecification(criteria.getId(), Foo_.id));
            }
            if (criteria.getName() != null) {
                specification = specification.and(buildStringSpecification(criteria.getName(), Foo_.name));
            }
        }
        return specification;
    }
}
