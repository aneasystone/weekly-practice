package com.example.demo.service;

import com.example.demo.service.dto.FooDTO;
import java.util.Optional;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;

/**
 * Service Interface for managing {@link com.example.demo.domain.Foo}.
 */
public interface FooService {
    /**
     * Save a foo.
     *
     * @param fooDTO the entity to save.
     * @return the persisted entity.
     */
    FooDTO save(FooDTO fooDTO);

    /**
     * Partially updates a foo.
     *
     * @param fooDTO the entity to update partially.
     * @return the persisted entity.
     */
    Optional<FooDTO> partialUpdate(FooDTO fooDTO);

    /**
     * Get all the foos.
     *
     * @param pageable the pagination information.
     * @return the list of entities.
     */
    Page<FooDTO> findAll(Pageable pageable);

    /**
     * Get the "id" foo.
     *
     * @param id the id of the entity.
     * @return the entity.
     */
    Optional<FooDTO> findOne(Long id);

    /**
     * Delete the "id" foo.
     *
     * @param id the id of the entity.
     */
    void delete(Long id);
}
