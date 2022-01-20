describe('match predictor', () => {
    it('compare two teams', () => {
        cy.visit('http://localhost:3010');

        cy.contains('Match Predictor').should('exist');

        cy.get('#home-team').select('Chelsea')
        cy.get('#away-team').select('Juventus')

        cy.contains('Submit').click()

        cy.contains('AWAY').should('exist')
    });
});
