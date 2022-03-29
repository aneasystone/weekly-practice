package com.example.demo.web.rest;

import com.example.demo.repository.FooRepository;
import com.example.demo.service.FooQueryService;
import com.example.demo.service.FooService;
import com.example.demo.service.criteria.FooCriteria;
import com.example.demo.service.dto.FooDTO;
import com.example.demo.web.rest.errors.BadRequestAlertException;
import java.net.URI;
import java.net.URISyntaxException;
import java.util.List;
import java.util.Objects;
import java.util.Optional;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.http.HttpHeaders;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.servlet.support.ServletUriComponentsBuilder;
import tech.jhipster.web.util.HeaderUtil;
import tech.jhipster.web.util.PaginationUtil;
import tech.jhipster.web.util.ResponseUtil;

/**
 * REST controller for managing {@link com.example.demo.domain.Foo}.
 */
@RestController
@RequestMapping("/api")
public class FooResource {

    private final Logger log = LoggerFactory.getLogger(FooResource.class);

    private static final String ENTITY_NAME = "foo";

    @Value("${jhipster.clientApp.name}")
    private String applicationName;

    private final FooService fooService;

    private final FooRepository fooRepository;

    private final FooQueryService fooQueryService;

    public FooResource(FooService fooService, FooRepository fooRepository, FooQueryService fooQueryService) {
        this.fooService = fooService;
        this.fooRepository = fooRepository;
        this.fooQueryService = fooQueryService;
    }

    /**
     * {@code POST  /foos} : Create a new foo.
     *
     * @param fooDTO the fooDTO to create.
     * @return the {@link ResponseEntity} with status {@code 201 (Created)} and with body the new fooDTO, or with status {@code 400 (Bad Request)} if the foo has already an ID.
     * @throws URISyntaxException if the Location URI syntax is incorrect.
     */
    @PostMapping("/foos")
    public ResponseEntity<FooDTO> createFoo(@RequestBody FooDTO fooDTO) throws URISyntaxException {
        log.debug("REST request to save Foo : {}", fooDTO);
        if (fooDTO.getId() != null) {
            throw new BadRequestAlertException("A new foo cannot already have an ID", ENTITY_NAME, "idexists");
        }
        FooDTO result = fooService.save(fooDTO);
        return ResponseEntity
            .created(new URI("/api/foos/" + result.getId()))
            .headers(HeaderUtil.createEntityCreationAlert(applicationName, true, ENTITY_NAME, result.getId().toString()))
            .body(result);
    }

    /**
     * {@code PUT  /foos/:id} : Updates an existing foo.
     *
     * @param id the id of the fooDTO to save.
     * @param fooDTO the fooDTO to update.
     * @return the {@link ResponseEntity} with status {@code 200 (OK)} and with body the updated fooDTO,
     * or with status {@code 400 (Bad Request)} if the fooDTO is not valid,
     * or with status {@code 500 (Internal Server Error)} if the fooDTO couldn't be updated.
     * @throws URISyntaxException if the Location URI syntax is incorrect.
     */
    @PutMapping("/foos/{id}")
    public ResponseEntity<FooDTO> updateFoo(@PathVariable(value = "id", required = false) final Long id, @RequestBody FooDTO fooDTO)
        throws URISyntaxException {
        log.debug("REST request to update Foo : {}, {}", id, fooDTO);
        if (fooDTO.getId() == null) {
            throw new BadRequestAlertException("Invalid id", ENTITY_NAME, "idnull");
        }
        if (!Objects.equals(id, fooDTO.getId())) {
            throw new BadRequestAlertException("Invalid ID", ENTITY_NAME, "idinvalid");
        }

        if (!fooRepository.existsById(id)) {
            throw new BadRequestAlertException("Entity not found", ENTITY_NAME, "idnotfound");
        }

        FooDTO result = fooService.save(fooDTO);
        return ResponseEntity
            .ok()
            .headers(HeaderUtil.createEntityUpdateAlert(applicationName, true, ENTITY_NAME, fooDTO.getId().toString()))
            .body(result);
    }

    /**
     * {@code PATCH  /foos/:id} : Partial updates given fields of an existing foo, field will ignore if it is null
     *
     * @param id the id of the fooDTO to save.
     * @param fooDTO the fooDTO to update.
     * @return the {@link ResponseEntity} with status {@code 200 (OK)} and with body the updated fooDTO,
     * or with status {@code 400 (Bad Request)} if the fooDTO is not valid,
     * or with status {@code 404 (Not Found)} if the fooDTO is not found,
     * or with status {@code 500 (Internal Server Error)} if the fooDTO couldn't be updated.
     * @throws URISyntaxException if the Location URI syntax is incorrect.
     */
    @PatchMapping(value = "/foos/{id}", consumes = { "application/json", "application/merge-patch+json" })
    public ResponseEntity<FooDTO> partialUpdateFoo(@PathVariable(value = "id", required = false) final Long id, @RequestBody FooDTO fooDTO)
        throws URISyntaxException {
        log.debug("REST request to partial update Foo partially : {}, {}", id, fooDTO);
        if (fooDTO.getId() == null) {
            throw new BadRequestAlertException("Invalid id", ENTITY_NAME, "idnull");
        }
        if (!Objects.equals(id, fooDTO.getId())) {
            throw new BadRequestAlertException("Invalid ID", ENTITY_NAME, "idinvalid");
        }

        if (!fooRepository.existsById(id)) {
            throw new BadRequestAlertException("Entity not found", ENTITY_NAME, "idnotfound");
        }

        Optional<FooDTO> result = fooService.partialUpdate(fooDTO);

        return ResponseUtil.wrapOrNotFound(
            result,
            HeaderUtil.createEntityUpdateAlert(applicationName, true, ENTITY_NAME, fooDTO.getId().toString())
        );
    }

    /**
     * {@code GET  /foos} : get all the foos.
     *
     * @param pageable the pagination information.
     * @param criteria the criteria which the requested entities should match.
     * @return the {@link ResponseEntity} with status {@code 200 (OK)} and the list of foos in body.
     */
    @GetMapping("/foos")
    public ResponseEntity<List<FooDTO>> getAllFoos(FooCriteria criteria, @org.springdoc.api.annotations.ParameterObject Pageable pageable) {
        log.debug("REST request to get Foos by criteria: {}", criteria);
        Page<FooDTO> page = fooQueryService.findByCriteria(criteria, pageable);
        HttpHeaders headers = PaginationUtil.generatePaginationHttpHeaders(ServletUriComponentsBuilder.fromCurrentRequest(), page);
        return ResponseEntity.ok().headers(headers).body(page.getContent());
    }

    /**
     * {@code GET  /foos/count} : count all the foos.
     *
     * @param criteria the criteria which the requested entities should match.
     * @return the {@link ResponseEntity} with status {@code 200 (OK)} and the count in body.
     */
    @GetMapping("/foos/count")
    public ResponseEntity<Long> countFoos(FooCriteria criteria) {
        log.debug("REST request to count Foos by criteria: {}", criteria);
        return ResponseEntity.ok().body(fooQueryService.countByCriteria(criteria));
    }

    /**
     * {@code GET  /foos/:id} : get the "id" foo.
     *
     * @param id the id of the fooDTO to retrieve.
     * @return the {@link ResponseEntity} with status {@code 200 (OK)} and with body the fooDTO, or with status {@code 404 (Not Found)}.
     */
    @GetMapping("/foos/{id}")
    public ResponseEntity<FooDTO> getFoo(@PathVariable Long id) {
        log.debug("REST request to get Foo : {}", id);
        Optional<FooDTO> fooDTO = fooService.findOne(id);
        return ResponseUtil.wrapOrNotFound(fooDTO);
    }

    /**
     * {@code DELETE  /foos/:id} : delete the "id" foo.
     *
     * @param id the id of the fooDTO to delete.
     * @return the {@link ResponseEntity} with status {@code 204 (NO_CONTENT)}.
     */
    @DeleteMapping("/foos/{id}")
    public ResponseEntity<Void> deleteFoo(@PathVariable Long id) {
        log.debug("REST request to delete Foo : {}", id);
        fooService.delete(id);
        return ResponseEntity
            .noContent()
            .headers(HeaderUtil.createEntityDeletionAlert(applicationName, true, ENTITY_NAME, id.toString()))
            .build();
    }
}
