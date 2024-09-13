/*
 * Copyright 2002-2016 the original author or authors.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package com.sqlsamples;

import static org.assertj.core.api.Assertions.*;

import java.util.List;

import org.junit.Test;
import org.junit.runner.RunWith;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;
import org.springframework.boot.test.autoconfigure.orm.jpa.TestEntityManager;
import org.springframework.test.context.junit4.SpringRunner;

/**
 * Some core unit tests verifying our custom finder using Spring Boot's "slice"-based test annotation
 * {@link DataJpaTest}.
 *
 * @author Rob Winch
 * @author Greg L. Turnquist
 */
@RunWith(SpringRunner.class)
@DataJpaTest
public class CustomerRepositoryTests {

	@Autowired
	private TestEntityManager entityManager;

	@Autowired
	private CustomerRepository customers;

	@Test
	public void testFindByLastName() {

		// given
		Customer customer = new Customer("first", "last");
		entityManager.persist(customer);

		// when
		List<Customer> findByLastName = customers.findByLastName(customer.getLastName());

		// then
		assertThat(findByLastName).extracting(Customer::getLastName).containsOnly(customer.getLastName());
	}
}