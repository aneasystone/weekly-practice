package com.example.demo.service.dto;

import java.io.Serializable;
import java.util.Objects;

/**
 * A DTO for the {@link com.example.demo.domain.Foo} entity.
 */
public class FooDTO implements Serializable {

    private Long id;

    private String name;

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) {
            return true;
        }
        if (!(o instanceof FooDTO)) {
            return false;
        }

        FooDTO fooDTO = (FooDTO) o;
        if (this.id == null) {
            return false;
        }
        return Objects.equals(this.id, fooDTO.id);
    }

    @Override
    public int hashCode() {
        return Objects.hash(this.id);
    }

    // prettier-ignore
    @Override
    public String toString() {
        return "FooDTO{" +
            "id=" + getId() +
            ", name='" + getName() + "'" +
            "}";
    }
}
