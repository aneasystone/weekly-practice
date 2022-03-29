package com.example.demo.service.mapper;

import com.example.demo.domain.Foo;
import com.example.demo.service.dto.FooDTO;
import org.mapstruct.*;

/**
 * Mapper for the entity {@link Foo} and its DTO {@link FooDTO}.
 */
@Mapper(componentModel = "spring", uses = {})
public interface FooMapper extends EntityMapper<FooDTO, Foo> {}
