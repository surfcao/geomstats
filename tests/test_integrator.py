"""Test for the integratos."""

import warnings

import tests.helper as helper

import geomstats.backend as gs
import geomstats.tests
from geomstats.geometry.euclidean import Euclidean
from geomstats.geometry.matrices import Matrices
from geomstats.geometry.general_linear import GeneralLinear
import geomstats.integrator as integrator


class TestIntegrator(geomstats.tests.TestCase):
    def setUp(self):
        self.dimension = 4
        self.dt = 0.1
        self.euclidean = Euclidean(self.dimension)
        self.matrices = Matrices(self.dimension)
        self.intercept = self.euclidean.random_uniform(1)
        self.slope = Matrices.make_symmetric(self.matrices.random_uniform(1))

    def function_linear(self, point, vector):
        return - gs.dot(self.slope, vector)

    def test_symplectic_euler_step(self):
        state = (self.intercept, self.slope)
        result = len(integrator._symplectic_euler_step(
            state, self.function_linear, self.dt))
        expected = len(state)

        self.assertAllClose(result, expected)

    def test_rk4_step(self):
        state = (self.intercept, self.slope)
        result = len(integrator.rk4_step(
            state, self.function_linear, self.dt))
        expected = len(state)

        self.assertAllClose(result, expected)

    def test_integrator_euler(self):
        initial_state = self.euclidean.random_uniform(2)

        def function(position, velocity):
            return gs.zeros_like(velocity)

        result = integrator.integrate(function, initial_state)
        expected = (initial_state[0] + initial_state[1], initial_state[1])

        self.assertAllClose(result, expected)
