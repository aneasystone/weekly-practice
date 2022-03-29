package com.example.demo.service.impl;

import com.example.demo.domain.Foo;
import com.example.demo.repository.FooRepository;
import com.example.demo.service.FooService;
import com.example.demo.service.dto.FooDTO;
import com.example.demo.service.mapper.FooMapper;
import java.util.Optional;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

/**
 * Service Implementation for managing {@link Foo}.
 */
@Service
@Transactional
public class FooServiceImpl implements FooService {

    private final Logger log = LoggerFactory.getLogger(FooServiceImpl.class);

    private final FooRepository fooRepository;

    private final FooMapper fooMapper;

    public FooServiceImpl(FooRepository fooRepository, FooMapper fooMapper) {
        this.fooRepository = fooRepository;
        this.fooMapper = fooMapper;
    }

    @Override
    public FooDTO save(FooDTO fooDTO) {
        log.debug("Request to save Foo : {}", fooDTO);
        Foo foo = fooMapper.toEntity(fooDTO);
        foo = fooRepository.save(foo);
        return fooMapper.toDto(foo);
    }

    @Override
    public Optional<FooDTO> partialUpdate(FooDTO fooDTO) {
        log.debug("Request to partially update Foo : {}", fooDTO);

        return fooRepository
            .findById(fooDTO.getId())
            .map(existingFoo -> {
                fooMapper.partialUpdate(existingFoo, fooDTO);

                return existingFoo;
            })
            .map(fooRepository::save)
            .map(fooMapper::toDto);
    }

    @Override
    @Transactional(readOnly = true)
    public Page<FooDTO> findAll(Pageable pageable) {
        log.debug("Request to get all Foos");
        return fooRepository.findAll(pageable).map(fooMapper::toDto);
    }

    @Override
    @Transactional(readOnly = true)
    public Optional<FooDTO> findOne(Long id) {
        log.debug("Request to get Foo : {}", id);
        return fooRepository.findById(id).map(fooMapper::toDto);
    }

    @Override
    public void delete(Long id) {
        log.debug("Request to delete Foo : {}", id);
        fooRepository.deleteById(id);
    }
}
