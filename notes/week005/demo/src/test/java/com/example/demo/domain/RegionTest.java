package com.example.demo.domain;

import static org.assertj.core.api.Assertions.assertThat;

import com.example.demo.web.rest.TestUtil;
import org.junit.jupiter.api.Test;

class RegionTest {

    @Test
    void equalsVerifier() throws Exception {
        TestUtil.equalsVerifier(Region.class);
        Region region1 = new Region();
        region1.setId(1L);
        Region region2 = new Region();
        region2.setId(region1.getId());
        assertThat(region1).isEqualTo(region2);
        region2.setId(2L);
        assertThat(region1).isNotEqualTo(region2);
        region1.setId(null);
        assertThat(region1).isNotEqualTo(region2);
    }
}
