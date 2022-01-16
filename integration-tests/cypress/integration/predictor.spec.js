describe('match predictor', () => {
    it('loads the main page', () => {
        cy.visit('http://localhost:3010');

        cy.contains('Match Predictor').should('exist');
    });
});
