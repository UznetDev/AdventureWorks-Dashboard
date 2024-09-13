package com.sqlsamples;

import java.util.List;

import org.springframework.data.repository.CrudRepository;

/**
 * Spring Data repository that uses Spring Data Commons platform neutral {@link CrudRepository} instead of
 * the JPA-specific {@link org.springframework.data.jpa.repository.JpaRepository}.
 *
 * @author Greg L. Turnquist
 */
public interface CustomerRepository extends CrudRepository<Customer, Long> {

	List<Customer> findByLastName(String lastName);
}
