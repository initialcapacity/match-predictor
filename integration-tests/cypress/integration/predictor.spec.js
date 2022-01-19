describe('match predictor', () => {
    it('compare two teams in the same country', () => {
        cy.visit('http://localhost:3010');

        cy.contains('Match Predictor').should('exist');

        cy.contains('Home').click().type('Chelsea')
        cy.contains('Away').click().type('Southampton')

        cy.contains('Submit').click()

        cy.contains('HOME').should('exist')
    });

    it('compare two teams in different countries', () => {
        cy.visit('http://localhost:3010');

        cy.contains('Match Predictor').should('exist');

        cy.contains('Home').click().type('Chelsea')
        cy.contains('Away').click().type('Juventus')

        cy.contains('Submit').click()

        cy.contains('AWAY').should('exist')
    });
});
