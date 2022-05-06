package com.example.demo.repository;

import com.example.demo.domain.Foo;
import org.springframework.data.jpa.repository.*;
import org.springframework.stereotype.Repository;

/**
 * Spring Data SQL repository for the Foo entity.
 */
@SuppressWarnings("unused")
@Repository
public interface FooRepository extends JpaRepository<Foo, Long>, JpaSpecificationExecutor<Foo> {}
